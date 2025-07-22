# Emopathy: A Centralized Hub for Emotion and Empathy Recognition

CKJ: **Graphics Placeholder**

> **"I do not ask the wounded person how he feels, I myself become the wounded person."**  
> – Walt Whitman, *Song of Myself*

---

Emotion and empathy are at the heart of human interaction, shaping how we understand and respond to one another. While emotion recognition has made significant strides in NLP and AI, driven by benchmark datasets like IEMOCAP, empathy remains underexplored due to the lack of standardized datasets and benchmarks. This paper provides an integrated summary of available resources for emotion and empathy-related tasks, including datasets, labeling conventions, and SOTA models. By synthesizing these elements, we aim to bridge existing gaps, introduce SOTA AI/ML models, and discuss implications and future directions to advance AI-driven understanding of human emotions and empathy.

Emopathy is a companion repository to this review paper, designed as a centralized hub for researchers. It consolidates the datasets, models, and insights discussed in the paper, offering a practical and insightful resource for fostering innovation and exploration in emotion and empathy recognition.

---

## Our Approach

To curate the content, we conducted an exhaustive review of **emotion** and **empathy** datasets and related AI/ML research. Our methodology included the following steps:

1. **Database Search**  
   We leveraged reputable sources such as **Scopus**, **Web of Science**, **ProQuest**, **ACM**, **Google Scholar**, and **ACL** to gather a comprehensive collection of publications.  

2. **Boolean Filtering**  
   Advanced search queries were employed to identify relevant works published after 2014. Scripts for this process are available:  
   - [Boolean Search Scripts](https://github.com/ninackjeong/emopathy-dataset-review/tree/main/boolean-search)  
   - [ACL Filtering Script](https://github.com/ninackjeong/emopathy-dataset-review/blob/main/filtering.py)  
   - [Filtering Script for Other Databases](https://github.com/ninackjeong/emopathy-dataset-review/blob/main/filtering.py)  

3. **(Semi-)Manual Screening**  
   The results were refined by (semi-)manual screening to ensure the datasets and papers met our quality and relevance criteria.


### Findings Overview
CKJ: Update numbers after finishing final screening!

- **Emotion Datasets**: Identified **FFF** datasets spanning text, audio, and video.  
- **Empathy Datasets**: Discovered **GGG** datasets, underscoring the need for further development.  
- **AI/ML Models**:  
  - Emotion recognition: **HHH** papers reviewed; top **XXX** models ranked by F1 scores.  
  - Empathy recognition: **III** papers identified; all models included due to limited research.  

---

## Trending Emotion/Empathy-related Tasks
CKJ: Forshadowing our future works!

We are currently analyzing emerging trends in emotion and empathy research. Expect updates on:  
- **Multimodal Emotion Recognition**: Integrating text, speech, and visual cues for enhanced context understanding.  
- **Empathy Prediction in Conversational AI**: Understanding human-like empathetic responses in dialogue systems.  
- **Applications in Healthcare**: Leveraging emotion and empathy recognition in mental health support, therapy, and patient care.  

---

## Table of Contents
- [Benchmark Datasets](#benchmark-datasets)  
  - [Emotion](#emotion)  
  - [Empathy](#empathy)  
- [SOTA ML Models](#sota-ml-models)  
  - [Emotion Recognition](#emotion-recognition)  
  - [Empathy Recognition](#empathy-recognition)  

---

## Benchmark Datasets
CKJ: We are working on this on [a separate sheet](https://docs.google.com/spreadsheets/d/1704Q1WFzSVgyDUeczfqA7h7QPOQgYPyXtyOO2MJmFHk/edit?gid=1071129490#gid=1071129490)

### Emotion
| Dataset | Author | Year	| Conversation Setting | Corpus Setting	| Modality | Source	| Labels | Annotation	| Statistics | Dataset Link | Paper Link |
| ------- | ------ | ---- | -------------------- | -------------- | -------- | ------ | ------ | ---------- | ---------- | ------------ | ---------- |
| IEMOCAP | Busso et al. | 2008 | Dyadic | Laboratory | Text/audio/video (facial/hand movements) | The use of plays (scripted sessions), and improvisation based hypothetical scenarios (spontaneous sessions) | <ul><li>Categorical: 8 emotions (Ekman's 7 emotions + neutral)</li><li>Continuous: activation, valency, etc.</li></ul> | Subjects after recording (self-assessment) & 6 human evaluators | <ul><li>ten actors (female 5, male 5) were recorded in dyadic sessions (5 sessions with 2 subjects each)</li><li>12 hours</li><li>10039 (scripted session: 5255 turns; spontaneous sessions: 4784 turns) with an average duration of 4.5 seconds. The average value of words per turn was 11.4.</li></ul> | [By request](https://sail.usc.edu/iemocap/index.html) | [IEMOCAP: Interactive emotion dyadic motion capture database](https://sail.usc.edu/iemocap/Busso_2008_iemocap.pdf) | <!-- rows 2- 33 go here> 
| BoLD | Yu Luo, et al. | 2018 | Emotional expression and body movement | Capture spontaneous bodily expressions in naturalistic settings | Visual (videos) | Diverse video sources to ensure a wide range of spontaneous bodily expressions | <ul><li>categorical</li><li>emotion categories</li></ul> | <ul><li>Annotations include emotional labels assigned to each video clip, focusing on perceived emotions based on body movements</li></ul> | <ul><li>Contains 9,876 video clips featuring 13,239 human characters</li></ul> | [Body Language Dataset](https://paperswithcode.com/dataset/bold) | [ARBEE: Towards Automated Recognition of Bodily Expression of Emotion In the Wild](https://arxiv.org/abs/1808.09568)|
| CMU-MultiPIE | Ralph Gross, et al. | 2008 | Facial images | Controlled lab environment, subjects were imaged under various conditions including different poses, illuminations and expressions | Visual (image data) | Collected at Carnegie Mellon University | <ul><li>Categorical</li><li>images were labeled based on subject idenitty, pose, illumination condition, and facial expression</li></ul> | <ul><li>Each image is annotated with metadata specifying the subject ID, camera viewpoint, illumination condition, and the type of facial expression displayed</li></ul> | <ul><li>Comprises over 750,000 images of 337 subjects, captured across up to 4 sessions over 5 months</li><li>337 subjects were captured under 15 viewpoints and 19 illumination conditions</li></ul> | [Database](https://www.cs.cmu.edu/afs/cs/project/PIE/MultiPie/Multi-Pie/Home.html) | [Multi-PIE](https://ieeexplore.ieee.org/document/4813399) |
| RAF-DB | Shan Li, Weihong Deng, and Jun Ping Du | 2017 | Static facial images | Real-world, unconstrained environments, images were collected from internet | Visual (static facial images) | Internet, encompassing diverse subjects in terms of age, gender, ethnicity, head poses, lighting conditions, and occlusions | <ul><li>categorical</li><li>based expressions or compound expression</li></ul> | <ul><li>Anger, disgust, fear, happiness, sadness, surprise, neutral</li><li>Each image was annotated by 40 independent taggers to ensure reliability</li></ul> | <ul><li>Contains 29,672 facial images with 15,339 images labeled with basic expressions and 14,33 images labeled with compound</li></ul> | [dataset](https://www.whdeng.cn/RAF/model1.html) | [Reliable Crowdsourcing and Deep Locality-Preserving Learning for Expression Recognition in the Wild](https://openaccess.thecvf.com/content_cvpr_2017/papers/Li_Reliable_Crowdsourcing_and_CVPR_2017_paper.pdf) |
 | iCV-MEFED | Jianfeg Guo, et al. | 2018 | Static facial images | Controlled lab environment, images captured under uniform lighting conditions with consistent background  | Visual (static facial images) | 125 subjects that are a balanced representation of genders and diverse ethnic backgrounds, aged between 18 and 37 years | <ul><li>categorical</li><li>each image is labeled with one of 50 compound emotion categories</li></ul> | <ul><li>Each image is annotated with a specific compound emotion label, combining a dominant and a complementary emotion</li><li>Labels were assessed and validated by psychologists to ensure accuracy</li></ul> | <ul><li>Contains 31,250 images with each of the 125 subjects contributing 250 images</li><li>5 samples for each of the 50 emotion categories</li></ul> |[dataset](https://www.researchgate.net/figure/Sample-of-different-emotion-categories-in-the-iCV-MEFED-dataset_fig2_370605669)|[Emotion Recognition Based on Facial Expressions Using Convolutional Neural Network (CNN)](https://ieeexplore.ieee.org/document/9302866)|
| AFEW | Abhinav Dhall, et al. | 2012 | Group (Acted facial expressions) | Movies | Audio-visual |||||[]()|[]()|
| KDEF | Daniel Lundqvist and Manuel Calvo |  1998 | Static facial images | Controlled lab environment | Visual (static facial images) |||||[]()|[]()|
| JAFFE | Lyons et al. | 1998 | Monadic | Controlled. Each expresser took pictures of herself while looking through a semi-reflective plastic sheet towards the camera. Tungsten lights were positioned to illuminate the face evenly. A box enclosed the region between the camera and plastic sheet to reduce back-reflection | Visual (images) |||||[]()|[]()|
| MMI | Pantic et al. | 2005 | Monadic |Controlled ~1/4 of samples had natural lighting and variable backgrounds were used. ~ 3/4 of samples used a blue screen background and two high-intensity lamps with reflective umbrellas | visual (image and videos) |||||[]()|[]()|
| BU-4DFE | Yin et al. | 2008 | Monadic | Controlled. Recording setup using a dynamic face capturing system | Dynamic 3D models created from a 3D video sequences. Resolution of approx. 35,000 vertices |||||[]()|[]()|
| BU-EEG | Li et al. | 2020 | Monadic | Controlled
Recording setup with 128 sensors around the participant's head to record EEG signals | EEG signals and videos |||||[]()|[]()|
| BP4D++ | Li et al. | 2023 | Monadic | Controlled recording setup | video and physiological measurements. 3D sequence, 2D RGB sequence, thermal sequence, and the sequences of physiological data (e.g., heart rate, blood pressure, skin conductance (EDA), and respiration rate), and meta-data (facial features and partially coded FACS) |||||[]()|[]()|
| CASME II | Yan et al. | 2014 | Monadic | Controlled laboratory environment | Visual (videos) |||||[]()|[]()|
| SFEW | Dhall et al. | 2011 | Monadic, dyadic, and group | Movie set | Visual and audio (videos) |||||[]()|[]()|
| DFEW | Jiang et al. | 2020 |  Monadic, dyadic, and group | Movie set | Visual and audio (videos) |||||[]()|[]()|
| GEMEP | Bänziger et al. | 2012 |  Monadic | Laboratory | Visual and audio (videos) |||||[]()|[]()|
| SEED-VII | Jiang et al. | 2024 | Monadic, dyadic, and group | Laboratory | EEG signals and eye movement |||||[]()|[]()|
| AMIGOS | Miranda-Correa et al. | 2021 | Monadic and group | Laboratory | EEG, ECG, and GSR signals |||||[]()|[]()|
| CreativeIT | Metallinou et al. | 2015 | Dyadic | Laboratory. Each actor wore a special body suit and 45 markers were placed across his/her body | Video and motion |||||[]()|[]()|
| DECAF | Abadi et al. | 2015 | Monadic | Laboratory | Magnetoencephalogram (MEG) signals, near-infra-red (NIR) facial videos, horizontal Electrooculogram (hEOG), Electrocardiogram (ECG), and trapezius-Electromyogram (tEMG) peripheral physiological responses |||||[]()|[]()|



### Empathy
| Dataset | Author | Year	| Conversation Setting | Corpus Setting	| Modality | Source	| Labels | Annotation	| Statistics | Dataset Link | Paper Link |
| ------- | ------ | ---- | -------------------- | -------------- | -------- | ------ | ------ | ---------- | ---------- | ------------ | ---------- |
| Five Factor Model | Lewis Goldberg | 1993 | N.A | Psycholexical analysis of personality descriptors from dictionaries and linguistic sources. | Textual – Analysis of written language descriptors. |||||[]()|[]()|
| Empathetic Dialogues (Facebook AI) 25k | Aravind Sesagiri Raamkumar and Yinping Yang | 2022 | Dyadic | The conversations were collected via Amazon Mechanical Turk, where crowd-workers were paired to engage in dialogues based on specific emotional situations. ||||||[]()|[]()|
| MEDIC | Zhou'an Zhu, Xin Li, et al. | 2023 | Face-to-face psychological counseling sessions between counselors and clients. | Video recordings of actual counseling sessions ||||||[]()|[]()|
| OMG-Empathy | Pablo Barros, Nikhil Churamani, Angelica Lim, and Stefan Wermter​ | 2019 | Dyadic | Video recordings of interactions between speakers and listeners, each lasting approximately 5 minutes, with speakers conveying one of eight different stories designed to elicit varying emotional responses. ||||||[]()|[]()|
| OMG-Empathy: Affective Faces | Scott Geng, Revant Teotia, Purva Tendulkar, Sachit Menon, and Carl Vondrick | 2023 | Dyadic | Video recordings ||||||[]()|[]()|
| Empathic Conversations: A Multi-level Dataset of Contextualized Conversations | Damilola Omitaomu, Shabnam Tafreshi, Tingting Liu, Sven Buechel, Chris Callison-Burch, Johannes Eichstaedt, Lyle Ungar, and João Sedoc | 2022 | Dyadic | Written information about pairs of participants engaging in discussions about provided news articles designed to elicit empathy and personal distress. ||||||[]()|[]()|
| LLM-GEm | Md Rakibul Hasan, Md Zakir Hossain, Tom Gedeon, Shafin Rahman | 2024 | N/A - includes only essays | College age Participants read newspaper articles and wrote essays reflecting their thoughts and feelings in response to the content. ||||||[]()|[]()|
| Empathy Detection from Text, Audiovisual, Audio or Physiological Signals: Task Formulations and Machine Learning Methods | Carlos Busso, Murtaza Bulut, Chi-Chun Lee, Abe Kazemzadeh, Emily Mower, Samuel Kim, Jeannette N. Chang, Sungbok Lee, Shrikanth S. Narayanan | 2008 | N/A does not introduce a new dataset | Recorded in a controlled environment with professional actors engaging in emotional dialogues. ||||||[]()|[]()|
| Modeling Empathy and Distress in Reaction to News Stories | Sven Buechel, Anneke Buffone, Barry Slaff, Lyle Ungar, and João Sedoc | 2018 | Individual written reactions (messages) to news articles, not conversations. | Participants read news articles and wrote short messages reflecting their reactions, which were then collected to form the dataset. ||||||[]()|[]()|
| Empathy-Mental-Health | Ashish Sharma, Adam S. Miner, David C. Atkins, and Tim Althoff​ | 2020 | Dyadic | Collected from online mental health platforms, specifically TalkLife and mental health-related subreddits, focusing on peer-to-peer support conversations. ||||||[]()|[]()|
| BAUM-1 | S. Zhalehpour, O. Onder, Z. Akhtar, and C. Eroglu Erdem | 2016 | Not applicable – The dataset consists of individual spontaneous reactions to visual stimuli, not conversations. | Participants were shown a sequence of images and short video clips designed to elicit specific emotions and mental states. They then expressed their feelings and thoughts about the stimuli in their own words, without using predetermined script ||||||[]()|[]()|
| 404 YouTube vloggers (194 M, 210 F)/ YouTube personality dataset | Javier B. Biel and Daniel Gatica-Perez | 2013 | Monologue – Vloggers speaking directly to the camera, sharing personal thoughts, opinions, or experiences. | Collected from publicly available YouTube vlogs where individuals explicitly show themselves in front of a webcam, discussing a variety of topics including personal issues, politics, movies, and books. ||||||[]()|[]()|
| 47 (27 M 20 F)/YouTube dataset | Javier B. Biel and Daniel Gatica-Perez | 2012 | Monologue – Vloggers speaking directly to the camera, sharing personal thoughts, opinions, or experiences. | Collected from publicly available YouTube vlogs where individuals explicitly show themselves in front of a webcam, discussing a variety of topics including personal issues, politics, movies, and books. ||||||[]()|[]()|
| ISEAR | Klaus R. Scherer and Harald Wallbott | 1994 | Not applicable – The dataset consists of individual self-reported experiences, not conversations | Participants from 37 countries provided written descriptions of situations in which they experienced specific emotions.​ ||||||[]()|[]()|
| 47 (27 M and 20 F)/YouTube dataset SenticNet | Louis-Philippe Morency, Rada Mihalcea, and Payal Joshi | 2011 | Monologue – Vloggers speaking directly to the camera, sharing personal opinions and reviews. | Collected from publicly available YouTube opinion videos where individuals express their sentiments on various topics. ||||||[]()|[]()|

---
<ul><li></li></ul>
<ul><li></li><li></li></ul>

## SOTA ML Models

### Emotion Recognition
The SOTA models for emotion recognition, ranked by F1 score:
- Categories: Transformer-based models, graph models, etc.  

### Empathy Recognition
A detailed list of empathy recognition models:
- Mostly regression tasks.


