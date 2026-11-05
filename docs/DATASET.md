# Dataset

ArSL Recognition uses the class layout of the **ArSL21L** dataset. The photos in the README's screenshots come from it too.

## ArSL21L: Arabic Sign Language Letter Dataset

| | |
|---|---|
| Creators | Ganzorig Batnasan, Munkhjargal Gochoo, Munkh-Erdene Otgonbold, Fady Alnajjar, Timothy K. Shih |
| Institution | United Arab Emirates University |
| Contents | 14,202 photos of 32 letter signs from 50 signers, with bounding-box annotations |
| Download | [Mendeley Data, version 1](https://data.mendeley.com/datasets/8hrn3bvdvk/1), DOI [10.17632/8hrn3bvdvk.1](https://doi.org/10.17632/8hrn3bvdvk.1) |
| License | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

**Citation**

> G. Batnasan, M. Gochoo, M.-E. Otgonbold, F. Alnajjar and T. K. Shih, "ArSL21L: Arabic Sign Language Letter Dataset Benchmarking and an Educational Avatar for Metaverse Applications," *2022 IEEE Global Engineering Education Conference (EDUCON)*, Tunis, Tunisia, 2022, pp. 1814–1821, doi: [10.1109/EDUCON52537.2022.9766497](https://doi.org/10.1109/EDUCON52537.2022.9766497).

The download is a single `data.zip`. Inside it, photos are in `data/sign_data/images/`, YOLO labels are in `data/sign_data/labels/`, and the official split is in `data/train.txt` and `data/val.txt`. File names follow `{signer}_{age}_{sex}_{letter}_{n}.jpg`.

## Photos used in this README

All screenshot photos are from the dataset's **validation split** and the same signer (`1003_19`), and are used under CC BY 4.0. **Changes made:** the white padding bars were trimmed and each photo was center-cropped to 4:3 before being shown in the app window. The app then drew the model's bounding box and label on top.

Unchanged copies of the original photos are in [`docs/samples/`](samples/).

### Screenshots

| Letter | File in `data.zip` | Copy |
|---|---|---|
| Meem (م) | `data/sign_data/images/1003_19_F_meem_0.jpg` | [view](samples/1003_19_F_meem_0.jpg) |
| Ain (ع) | `data/sign_data/images/1003_19_F_ain_0.jpg` | [view](samples/1003_19_F_ain_0.jpg) |
| Alef (ا) | `data/sign_data/images/1003_19_F_aleff_0.jpg` | [view](samples/1003_19_F_aleff_0.jpg) |
| Thal (ذ) | `data/sign_data/images/1003_19_F_thal_0.jpg` | [view](samples/1003_19_F_thal_0.jpg) |
| Al (ال) | `data/sign_data/images/1003_19_F_al_0.jpg` | [view](samples/1003_19_F_al_0.jpg) |
| Ba (ب) | `data/sign_data/images/1003_19_F_bb_0.jpg` | [view](samples/1003_19_F_bb_0.jpg) |

### Demo animation

The animation at the top of the README shows letters in Arabic alphabetical order, signed by seven different participants. The photos were shown unchanged, apart from trimming the white padding bars.

| Letter | File in `data.zip` | Split |
|---|---|---|
| Alef (ا) | `data/sign_data/images/1011_37_F_aleff_0.jpg` | validation |
| Ba (ب) | `data/sign_data/images/1008_28_F_bb_0.jpg` | training |
| Ta (ت) | `data/sign_data/images/1004_19_M_ta_2.jpg` | training |
| Thaa (ث) | `data/sign_data/images/1020_22_M_thaa_7.jpg` | training |
| Jeem (ج) | `data/sign_data/images/7_21_M_jeem_3.jpg` | training |
| Haa (ح) | `data/sign_data/images/2_20_M_haa_4.jpg` | training |
| Khaa (خ) | `data/sign_data/images/1004_19_M_khaa_6.jpg` | training |
| Ain (ع) | `data/sign_data/images/1201_23_M_ain_7.jpg` | training |
