import os
import json
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
import pandas as pd
import clip


def load_image_paths(directory, extensions=('png', 'jpg', 'jpeg')):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(extensions)]

def save_json(data, output_path):
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f'Data saved to {output_path}')

def save_numpy(data, output_path):
    np.save(output_path, data)
    print(f'Array saved to {output_path}')

def load_cub_dataset(data_dir):
    images = pd.read_csv(os.path.join(data_dir, 'images.txt'), sep=' ', names=['image_id', 'file_path'])
    labels = pd.read_csv(os.path.join(data_dir, 'image_class_labels.txt'), sep=' ', names=['image_id', 'class_id'])
    classes = pd.read_csv(os.path.join(data_dir, 'classes.txt'), sep=' ', names=['class_id', 'class_name'])
    bounding_boxes = pd.read_csv(os.path.join(data_dir, 'bounding_boxes.txt'), sep=' ', names=['image_id', 'x', 'y', 'width', 'height'])
    part_locs = pd.read_csv(os.path.join(data_dir, 'parts/part_locs.txt'), sep=' ', names=['img_id', 'part_id', 'x', 'y', 'visible'])
    # parts = pd.read_csv(os.path.join(data_dir, 'parts/parts.txt'), delimiter =' ', names=['part_id', 'part_name'])
    parts = pd.read_fwf(os.path.join(data_dir, 'parts/parts.txt'), colspecs=[(0, 2), (2, None)], header=None, names=['part_id', 'part_name'])
    parts_click_locs = pd.read_csv(os.path.join(data_dir, 'parts/part_click_locs.txt'), sep = ' ', names=['image_id', 'part_id', 'x', 'y', 'visible', 'time'])
    attributes = pd.read_csv(os.path.join(data_dir, 'attributes/attributes.txt'), sep = ' ', names=['attribute_id', 'attribute_name'])
    certainties = pd.read_fwf(os.path.join(data_dir, 'attributes/certainties.txt'), colspecs=[(0, 1), (2, None)], names=["certainty_id", "certainty_name"])
    image_attribute_labels = pd.read_csv(os.path.join(data_dir, 'attributes/image_attribute_labels.txt'),
                                             # sep = ' ',
                                             names=['image_id', 'attribute_id', 'is_present', 'certainty_id', 'time'],
                                             delim_whitespace=True, usecols=range(5)
                                            )
    with open(os.path.join(data_dir, 'llava_captions.json'), 'r') as f:
        llava_captions = json.load(f)
    return images, labels, classes,  bounding_boxes, parts, part_locs, parts_click_locs, attributes, certainties, image_attribute_labels, llava_captions

def get_clip_image_features(model, preprocess, image_path, device):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model.encode_image(image).cpu().numpy()
    return features

def get_clip_text_features(model, text, device):
    text_inputs = clip.tokenize([text]).to(device)
    with torch.no_grad():
        features = model.encode_text(text_inputs).cpu().numpy()
    return features


def get_clip_similarity_score(img_features, text_features):
    img_features /= img_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity_score = (100.0 * img_features @ text_features.T).softmax(dim=-1)
    return similarity_score.item()

def recognize_bird_species(img_path, classes):
    img_features = get_clip_image_features(img_path)
    similarities = []
    for class_name in classes['class_name']:
        text_features = get_clip_text_features(class_name)
        similarity_score = get_clip_similarity_score(img_features, text_features)
        similarities.append((class_name, similarity_score))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[0][0]

def get_cosine_similarity(img_features: torch.Tensor, txt_features: torch.Tensor) -> torch.Tensor:

    img_features = img_features.squeeze()
    txt_features = txt_features.squeeze()
    
    dot_product = torch.dot(img_features, txt_features)
    
    norm_img = torch.norm(img_features, p=2)
    norm_txt = torch.norm(txt_features, p=2)
    
    # Avoid division by zero
    if norm_img == 0 or norm_txt == 0:
        return torch.tensor(0.0)  # Handle zero-vector cases
    
    similarity = dot_product / (norm_img * norm_txt)
    
    return similarity.item()

def get_clip_llava_caption_features(text):
    sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]
    text_features = np.zeros((1, 512))
    for sentence in sentences:
        text_features += get_clip_text_features(sentence)
    text_features /= len(sentences)
    return text_features

def generate_clip_embeddings_imgs(data_dir, transform, images):
    img_dir = os.path.join(data_dir, 'images')    
    clip_embeds = np.zeros((11788, 512))
    for img_idx in tqdm(range(1, 11789)):
        img_path = images[images['image_id'] == img_idx]['file_path'].iloc[0]
        clip_embeds[img_idx - 1, :] = get_clip_image_features(os.path.join(img_dir, img_path), transform).squeeze()
    return clip_embeds

def generate_clip_embeddings_text(data_dir, llava_captions):
    clip_embeds = np.zeros((11788, 512))
    for img_idx in tqdm(range(1, 11789)):
        llava_caption = llava_captions[str(img_idx)]['llava_text']
        clip_embeds[img_idx-1, :] = get_clip_llava_caption_features(llava_caption)
    return clip_embeds