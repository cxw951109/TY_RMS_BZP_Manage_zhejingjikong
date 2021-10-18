from sqlalchemy import Column, String, create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.elements import BinaryExpression,BooleanClauseList
from sqlalchemy.sql import func
import traceback
import paginate_sqlalchemy
from sqlalchemy.pool import NullPool


"""数据仓储类"""
class Repository(object):

    # 初始化数据库连接
    # engine = create_engine('mysql+pymysql://root:123456@127.0.0.1/TY_RMS_Multiple?charset=utf8',
    engine = create_engine('mysql+pymysql://root:yyzk@127.0.0.1/ty_standard_talons_yanshi?charset=utf8',
                           pool_recycle=10600, pool_size=100, max_overflow=20)
    # 创建session工厂
    DBSession = sessionmaker(bind=engine)
    # 创建session对象
    session = DBSession()
    # 事务标识
    transFlag = False
    def __init__(self,entityType):
        super().__init__()
        # 对象类型
        self.entityType = entityType

    # 开始事务
    def beginTrans(self):
        self.session = self.DBSession()
        self.transFlag = True

    # 提交事务
    def commitTrans(self):
        try:
            self.transFlag = False
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            self.session.rollback()
            return False
        finally:
            self.session.close()

    # 新增数据
    def insert(self, entity):
        try:
            if (not self.transFlag):
                self.session = self.DBSession()
            self.session.add(entity)
            if(not self.transFlag):
                self.session.commit()
            return True
        except Exception as e:
            print(e, 88888888888)
            self.session.rollback()
            return False
        finally:
            self.session.close()
            
    # 新增多行数据
    def insert_many(self, entity_list):
        try:
            if(not self.transFlag):
                self.session=self.DBSession()
            self.session.bulk_save_objects(entity_list)
            if (not self.transFlag):
                self.session.commit()
                return True
        except Exception as e:
            flag_ = False
            self.session.rollback()
            return flag_
        finally:
            self.session.close()


    # 更新数据
    def update(self,entity):
        try:
            self.session=self.DBSession()
            self.session.merge(entity)
            if(not self.transFlag):
                self.session.commit()
            return True
        except Exception as e:
            print('ggggg',str(e))
            self.session.rollback()
            return False
        finally:
            self.session.close()


    # 删除操作
    def delete(self,where):
        try:
            if (not self.transFlag):
                self.session = self.DBSession()
            self.session.query(self.entityType).filter(where).delete()
            if(not self.transFlag):
                self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()


    # 查询单个实体
    def findEntity(self,*where):
        try:
            self.session=self.DBSession()
            if (type(*where) is BinaryExpression or type(*where) is BooleanClauseList):
                return self.session.query(self.entityType).filter(*where).first()
            else:
                return self.session.query(self.entityType).get(where)
        except Exception as e:
            print(e, 555555555555)
            self.session.rollback()
        finally:
            self.session.close()


    # 查询实体列表
    def findList(self,*where):
        try:
            self.session=self.DBSession()
            return self.session.query(self.entityType).filter(*where)
        except:
            self.session.rollback()
        finally:
            self.session.close()


    # 查询分页
    def queryPage(self,orm_query,pageParam):
        try:
            page = paginate_sqlalchemy.SqlalchemyOrmPage(orm_query,page=pageParam.curPage,items_per_page=pageParam.pageRows,db_session=self.DBSession)
            pageParam.totalRecords = page.item_count
            return page.items
        except Exception as e:
            raise e


    # 查询数量
    def findCount(self,*where):
        try:
            self.session=self.DBSession()
            return self.session.query(func.count('*')).select_from(self.entityType).filter(*where).scalar()
        except:
            self.session.rollback()
        finally:
            self.session.close()


    # 查询最大数
    def findMax(self,prop,*where):
        try:
            self.session=self.DBSession()
            return self.session.query(func.max(prop)).select_from(self.entityType).filter(*where).scalar()
        except:
            self.session.rollback()
        finally:
            self.session.close()


    # 执行Sql语句
    def execute(self,sql,*agrs):
        try:
            self.session=self.DBSession()
            return self.session.execute(sql,*agrs)
        except:
            self.session.rollback()
        finally:
            self.session.close()

    # 执行Sql语句
    def executeNoParam(self,sql):
        try:
            self.session=self.DBSession()
            self.session.execute(sql)
            if(not self.transFlag):
                self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()


