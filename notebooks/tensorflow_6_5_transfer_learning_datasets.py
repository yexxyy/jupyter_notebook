
# coding: utf-8

# ## 迁移学习概念
# 
# >将一个问题上训练好的模型通过简单的调整，使其使用于一个新的问题。利用新的数据集，通过训练好的神经网络对图像进行特征提取，然后再将提取的特征向量作为输入来训练一个新的单层全连接神经网络，以此实现新的分类问题
# 
# ### 数据集处理部分
# 
# [点击下载数据集](http://download.tensorflow.org/example_images/flower_photos.tgz)
# 
# page 162
# 
# ### 写在后面
# 
# 下面代码中
# ```
# for file_name in file_list:
#             image_raw_data=gfile.FastGFile(file_name,'rb').read()
#             image=tf.image.decode_jpeg(image_raw_data)
#             if image.dtype != tf.float32:
#                 image=tf.image.convert_image_dtype(image,dtype=tf.float32)
#             image=tf.image.resize_images(image,[299,299])
#             image_value=sess.run(image)
#             #print image_value.shape #(299, 299, 3)
# ```
# 实现了将图片处理成299 x 299 的三维数组，后来通过tensorboard看了inception-v3的机构图之后才发现这样的数据是对应张量 sub:0
# 
# 最开始的数据入口 DecodeJpeg:0 其实是可以直接输入图片的
# 
#  ![](https://upload-images.jianshu.io/upload_images/1271438-f0b3c008df4e2e04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# In[ ]:


import glob #查找符合特定规则的文件路径名
import os
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

INPUT_DATA='flower_photos'
#numpy格式
OUTPUT_FILE='flower_photos/flower_processed.npy'

#测试数据和验证数据比例
VALIDATION_PERCENTAGE=10
TEST_PERCENTAGE=10


# In[ ]:


#读取数据并将数据风格层训练数据／验证数据／测试数据

def create_image_lists(sess,testing_percentage,validation_percentage):
     
    sub_dirs=[x[0] for x in os.walk(INPUT_DATA)]
    # print sub_dirs
    """
    ['flower_photos',
     'flower_photos/daisy',
     'flower_photos/dandelion',
     'flower_photos/roses',
     'flower_photos/sunflowers',
     'flower_photos/tulips']
    """

    #初始化各个数据集
    training_images=[]
    training_labels=[]
    testing_images=[]
    testing_labels=[]
    validation_images=[]
    validation_labels=[]
    current_label=0


    file_list=[]
    for sub_dir in sub_dirs[1:]:
        dir_name = os.path.basename(sub_dir)

        #构造匹配图片文件路径
        #flower_photos/daisy/*.jpg
        file_glob=os.path.join(sub_dir,'*.'+'jpg')

        #匹配出文件列表
        #['flower_photos/tulips/100930342_92e8746431_n.jpg',....]
        file_names=glob.glob(file_glob)
        file_list.extend(file_names)

        #print file_list
        """
        ['flower_photos/daisy/100080576_f52e8ee070_n.jpg',
         'flower_photos/daisy/10140303196_b88d3d6cec.jpg',
         'flower_photos/daisy/10172379554_b296050f82_n.jpg',
         'flower_photos/daisy/10172567486_2748826a8b.jpg',
         'flower_photos/daisy/10172636503_21bededa75_n.jpg']
        """

        #处理图片数据
        #处理成299 x 299 以便inception-v3接收

        current_label=0
        """
        0-daisy(雏菊)
        1-dandelion（蒲公英）
        2-roses
        3-sunflowers
        4-tulips（郁金香）
        """

        for file_name in file_list:
            image_raw_data=gfile.FastGFile(file_name,'rb').read()
            image=tf.image.decode_jpeg(image_raw_data)
            if image.dtype != tf.float32:
                image=tf.image.convert_image_dtype(image,dtype=tf.float32)
            image=tf.image.resize_images(image,[299,299])
            image_value=sess.run(image)
            #print image_value.shape #(299, 299, 3)
            
            #随机划分数据集
            chance=np.random.randint(100)
            if chance < validation_percentage:
                validation_images.append(image_value)
                validation_labels.append(current_label)
            elif chance < (validation_percentage+testing_percentage):
                testing_images.append(image_value)
                testing_labels.append(current_label)
            else:
                training_images.append(image_value)
                training_labels.append(current_label)
        
        current_label+=1
        
    #将训练数据随机打乱
    state=np.random.get_state()
    np.random.shuffle(training_images)
    np.random.set_state(state)
    np.random.shuffle(training_labels)
    
    return np.asarray([training_images,training_labels,
                       validation_images,validation_labels,
                       testing_images,testing_labels])

def main():
    with tf.Session() as sess:
        processed_data=create_image_lists(sess,TEST_PERCENTAGE,VALIDATION_PERCENTAGE)
        #保存为numpy格式
        np.save(OUTPUT_FILE,processed_data)
        
if __name__=='__main__':
    main()

