#coding: utf8
import wtforms

class BaseForm(wtforms.Form):

    def get_error(self):
        if self.errors:
            # 随机获取一个字段的错误
            _,error = self.errors.popitem()
            # 将该字段的第一个错误拿出来
            return error[0]
        return None

