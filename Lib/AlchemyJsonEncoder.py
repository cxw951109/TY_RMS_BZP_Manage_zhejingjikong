from sqlalchemy.ext.declarative import DeclarativeMeta
import datetime
import decimal
import json

#sqlalchemy对象编码转换类
class AlchemyEncoder(json.JSONEncoder):
    #def _iterencode(self, o, markers=None):
    #    if isinstance(o, decimal.Decimal):
    #        return str(o)
    #    return super(AlchemyEncoder, self)._iterencode(o, markers)
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj.__class__, DeclarativeMeta):
            #SQLAlchemy类
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # 序列化对象
                    fields[field] = data
                    if data is None:
                        fields[field]=''
                except TypeError:    # 添加了对datetime的处理
                    if data is None:
                        fields[field]=''
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = str(data)
                    else:
                        fields[field] = None
            # Json编码字典
            return fields

        return json.JSONEncoder.default(self, obj)

