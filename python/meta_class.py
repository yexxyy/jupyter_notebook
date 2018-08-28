"""
元类编程
1)拦截类的创建
2)修改类
3)返回修改之后的类

元类是创建类的类
object <- class <- type
"""
#方式一
class BaseUser():
    pass

def say(self):
    print('say something...')

User=type('User',(BaseUser,),{'name':'jim','say':say})
user=User()
user.say()


#方式二
class MetaClass(type):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls,*args,**kwargs)


class MetaUser(metaclass=MetaClass):
    """
    python中类的实例化过程，会首先寻找metaclass，通过metaclass去创建user类
    如果本身及基类都没有设置metaclass则使用默认的type进行类的创建
    """
    
    
    def __init__(self,name):
        self.name=name
        
    def __str__(self):
        return self.name
    
    def __getattribute__(self, item):
        """属性访问入口"""
        print('__getattribute__{}'.format(item))
        return super(MetaUser, self).__getattribute__(item)
    
    def __getattr__(self, item):
        """找不到属性进入此方法"""
        if item=='nickname':
            return 'my nickname'
        return super(MetaUser, self).__getattr__(item)
    
    
#抽象基类
from collections.abc import *



#orm
from django.db.models import Model
import numbers

class Field():
    pass

class IntergerField(Field):
    def __init__(self,min_value=None,max_value=None):
        self.value=None
        self.min_value=min_value
        self.max_value=max_value
    
    def __get__(self, instance, owner):
        return self.value
    
    def __set__(self, instance, value):
        if not isinstance(value,numbers.Integral):
            raise ValueError('请传入数字')
        if self.min_value and self.min_value > value:
            raise ValueError('必须大于最小值')
        if self.max_value and self.max_value < value:
            raise ValueError('必须小于最大值')
        self.value=value
        

class CharField(Field):
    def __init__(self,max_length):
        self.value=None
        self.max_length=max_length
    
    def __get__(self, instance, owner):
        return self.value
    
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError('请传入字符串')
        if len(value) > self.max_length:
            raise ValueError('字符串长度超过{}'.format(self.max_length))
        self.value = value




class UserMetaClass(type):

    def __new__(cls,name,bases,attrs, **kwargs):
        if name=='BaseModel':
            return super().__new__(cls,name,bases,attrs, **kwargs)
        
        
        fields={}
        for key,value in attrs.items():
            if isinstance(value,Field):
                fields[key]=value
        attrs_meta=attrs.get('Meta',None)
        _meta={}
        db_table=name.lower()
        if attrs_meta:
            table=getattr(attrs_meta,'db_table',None)
            if table:
                db_table=table
                
        _meta['db_table']=db_table
        attrs['_meta']=_meta
        attrs['fields']=fields
        del attrs['Meta']

        return super().__new__(cls,name,bases,attrs, **kwargs)



class BaseModel(metaclass=UserMetaClass):
    def __init__(self,*args,**kargs):
        for key,value in kargs.items():
            setattr(self,key,value)
        return super(BaseModel, self).__init__()
    
    
    def save(self):
        fields=[]
        values=[]
        for key,value in self.fields.items():
            fields.append(key)
            values.append(str(value.value))
        sql='INSERT {db_table}({fields}) VALUE ({values})'.format(
            db_table=self._meta['db_table'],
            fields=','.join(fields),
            values=','.join(values)
        )
        print(sql)
        #INSERT user_table(name,age) VALUE (xan,3)
        


class User(BaseModel):

    class Meta:
        db_table='user_table'
    
    name=CharField(max_length=5)
    age= IntergerField(min_value=0,max_value=10)
    

    
if __name__ == '__main__':
    meta_user=MetaUser('xiao qiang')
    print(meta_user,meta_user.nickname)
    
    # user=User()
    # user.name='xande'
    # user.age=5
    
    #针对这样的赋值，需要在def __init__中处理，所以新建一个BaseModel
    user=User(name='xan',age=3)
    user.save()
    print(user.name,user.age)
    