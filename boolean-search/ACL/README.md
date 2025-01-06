# ACL Paper Search and Screening

## Step 1: Download Full Anthology

- **Format**: BibTeX with abstracts
- **Total Papers**: 97,446 (as of 08/05/2024)
- **Reference**: Hasan et al. 2024 reported 46,079 papers

## Step 2: Boolean Search with BibTeX

**Notebook**: `acl_boolean_search.ipynb`

### Search Strings:

#### Empathy
- **Query**: `empath* AND (detect* OR recog* OR predict* OR classi*)`
- **Results**: 101 papers 
- **Output**: `acl_empathy_related_papers.csv`

#### Emotion
- **Query**: `emot* AND (detect* OR recog* OR predict* OR classi*)`
- **Results**: 1,053 papers
- **Output**: `acl_emotion_related_papers.csv`

## Step 3: Create Zotero Items

**Notebook**: `acl_zotitem.ipynb`

- **Action**: Download PDF files locally and create Zotero items

### Local PDF Storage:
- **Empathy Papers**: Saved in the `ACL-EMPATHY` folder in our Zotero library
- **Emotion Papers**: Saved in the `ACL-EMOTION` folder in our Zotero library
