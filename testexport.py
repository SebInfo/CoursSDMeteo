#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[8]:


df = pd.read_csv("meteoMontpellier.csv", sep=";")


# In[12]:


df["validity_time"] = pd.to_datetime(df["validity_time"])


# In[13]:


df["validity_time"].dt.year.min(), df["validity_time"].dt.year.max()


# In[14]:


df_post_2017 = df[df["validity_time"].dt.year >= 2018]

df_post_2017["ww"].value_counts(dropna=False).head(10)


# In[15]:


get_ipython().system('ls')


# In[16]:


get_ipython().system('cd donnees')


# In[17]:


get_ipython().system('ls')


# In[ ]:




