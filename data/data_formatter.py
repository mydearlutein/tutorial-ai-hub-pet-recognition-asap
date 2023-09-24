import csv
import json
import os


def main(data_path: str = './dog_sample/training'):

    # actions = ['BODYLOWER','BODYSCRATCH','BODYSHAKE','FEETUP','FOOTUP','HEADING','LYING','MOUNTING','SIT','TAILING','TAILLOW','TURN','WALKRUN']
    actions = ['BODYLOWER','FOOTUP']
    headers = ['image'] + [element for pair in [(f'{i}_x', f'{i}_y') for i in range(15)] for element in pair]

    rows = []
    for action in actions:
        base_image_path = os.path.join(data_path, 'image', action)
        if not os.path.exists(base_image_path):
            continue

        base_label_path = os.path.join(data_path, 'label', action)
        label_files = os.listdir(base_label_path)

        for label_fname in label_files:
            with open(os.path.join(base_label_path, label_fname), 'r') as f:
                label = json.load(f)
                for anno in label['annotations']:
                    if label_fname.startswith('dog'):
                        image_fname = f"{label_fname.split('.json')[0]}/frame_{anno['frame_number']}_timestamp_{anno['timestamp']}.jpg"
                    else:
                        image_fname = f"{label_fname.replace('json', 'mp4')}/frame_{anno['frame_number']}_timestamp_{anno['timestamp']}.jpg"

                    check_fname = os.path.join(base_image_path, image_fname)
                    if not os.path.isfile(check_fname) or not os.path.exists(check_fname):
                        print(f'File not found: {check_fname}.. skipped!')
                        continue
                
                    row = [f"{action}/{image_fname}"]
                    keypoints = [p for kp in [(v['x'], v['y']) for k, v in anno['keypoints'].items() if v] for p in kp]
                    rows.append(row + keypoints)

    new_anno_file = os.path.join(data_path, f'data_annotation.csv')
    with open(new_anno_file, 'w') as new_f:
        writer = csv.writer(new_f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f'Created: {new_anno_file}, row count: {len(rows)}')

if __name__ == '__main__':
    main()