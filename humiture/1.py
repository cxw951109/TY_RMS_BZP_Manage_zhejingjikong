"""
 humiture_type = request.GET.get('type')
        # 判断是否传参  没有传参默认 humiture_type = '1'
        if not humiture_type or humiture_type == '1':
            startData = request.GET.get('startDate', '')
            endData = request.GET.get('endDate', '')
            # 搜索框的值
            searchValue = request.GET.get('searchValue', '')
            # ajax传过来的参数
            params = json.loads(request.GET.get('params', ''))
            startIndex = params['startIndex']
            pageSize = params['pageSize']
            page = params['page']
            # 实例化一个对象
            pageParam = PageParam(page, pageSize, orderType=desc)
            data = BllHumitureRecord().queryPage(
                BllHumitureRecord().findList(and_(EntityLog.OperateDate > startData, EntityLog.OperateDate < endData)).get_temperature_or_humidity(),
                pageParam)
            return JsonResponse(
                {'data': json.loads(Utils.resultAlchemyData(data))[:5], 'total': pageParam.totalRecords})


"""
