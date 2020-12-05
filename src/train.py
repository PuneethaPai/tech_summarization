import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from pathlib import Path

data_dir = Path("/kaggle/input/tldr-summary-for-man-pages/")
all_df = pd.concat([pd.read_csv(file) for file in data_dir.glob("*.csv")], ignore_index=True)

docs = all_df.loc[:, ["man_entry","doc_text"]].apply(lambda row: row.man_entry if not pd.isna(row.man_entry) else row.doc_text, axis=1)
docs.dropna(inplace=True)

all_df.count()

summary = all_df.tldr_summary[docs.index]
summary.shape, summary.count()

processed_df = pd.DataFrame(dict(text=docs, summary=summary))
processed_df.head()

processed_df.count()


########### Creating Batch loaders

import nlp
import pandas as pd
from fastai.text.all import *
from transformers import *

from blurr.data.all import *
from blurr.modeling.all import *

pretrained_model_name = "facebook/bart-large-cnn"
hf_arch, hf_config, hf_tokenizer, hf_model = BLURR_MODEL_HELPER.get_hf_objects(pretrained_model_name, 
                                                                               model_cls=BartForConditionalGeneration)

hf_arch, type(hf_config), type(hf_tokenizer), type(hf_model)
hf_batch_tfm = HF_SummarizationBeforeBatchTransform(hf_arch, hf_tokenizer, max_length=[256, 130])

blocks = (HF_TextBlock(before_batch_tfms=hf_batch_tfm, input_return_type=HF_SummarizationInput), noop)
dblock = DataBlock(blocks=blocks, 
                   get_x=ColReader('text'), 
                   get_y=ColReader('summary'), 
                   splitter=RandomSplitter())

dls = dblock.dataloaders(processed_df, bs=2)
len(dls.train.items), len(dls.valid.items)

b = dls.one_batch()
len(b), b[0]['input_ids'].shape, b[1].shape

dls.show_batch(dataloaders=dls, max_n=2)

text_gen_kwargs = { **hf_config.task_specific_params['summarization'], **{'max_length': 130, 'min_length': 30} }
text_gen_kwargs

###################### Training

model = HF_BaseModelWrapper(hf_model)
model_cb = HF_SummarizationModelCallback(text_gen_kwargs=text_gen_kwargs)

learn = Learner(dls, 
                model,
                opt_func=ranger,
                loss_func=CrossEntropyLossFlat(),
                cbs=[model_cb],
                splitter=partial(summarization_splitter, arch=hf_arch)).to_fp16()

learn.create_opt() 
learn.freeze()

learn.lr_find(suggestions=True)
b = dls.one_batch()
preds = learn.model(b[0])
len(preds),preds[0], preds[1].shape

learn.fine_tune(1)

learn.show_results(learner=learn, max_n=2)

################# Saving and Prediction

model_file = Path('models/bart_tldr.pkl')
learn.export(fname=model_file)

inf_learn = load_learner(fname=model_file)
inf_learn.blurr_summarize(test_article)