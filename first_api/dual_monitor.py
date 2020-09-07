@action(detail=True, methods=['post'])
    def testObservation(self, request):
        """ Test def"""
        data = request.data
        
        isExistPO = models.PointObservation.objects.filter(observation_village=data['observation_village'], observation_zone=data['observation_zone'], observation_work=data['observation_work'], observation_secure=data['observation_secure'], observation_date=data['observation_date']).exists()
        
        
        if(isExistPO==True):
            ## already have pointObservation
            pointObservation = models.PointObservation.objects.only('pk').get(observation_village=data['observation_village'], observation_zone=data['observation_zone'], observation_work=data['observation_work'], observation_secure=data['observation_secure'], observation_date=data['observation_date'])
            pointPkList = models.Checkpoint.objects.filter(point_zone=data['observation_zone'],is_active=True, point_active=True).values_list('pk', flat=True)
            for pointPk in pointPkList: ## all point 
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=pointPk)
                isExistPOPL = models.PointObservationPointList.objects.filter(observation_pk=pointObservation, checkpoint_pk=checkpoint).exists()
                if(isExistPOPL==False):
                    pointObservationPointList = models.PointObservationPointList.objects.create(observation_pk=pointObservation, checkpoint_pk = checkpoint)
                    pointObservationPointList.save()

            ## check the exist PointObservationRecord
            isExistPOR = models.PointObservationRecord.objects.filter(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk']).exists()
            if(isExistPOR==True):
                ## already have pointObservationRecord
                pointObservationRecord = models.PointObservationRecord.objects.only('pk').get(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk'])
                return Response({ "detail": 'already have this pointObservation and pointObservationRecord'},status=status.HTTP_200_OK)
            else:
                ## create new  pointObservationRecord
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=data['checkpoint_pk'])
                pointObservationRecord = models.PointObservationRecord.objects.create(observation_checkin_time=data['observation_checkin_time'], observation_checkout_time=data['observation_checkout_time'],observation_timeslot=data['observation_timeslot'],checkpoint_pk = checkpoint, observation_pk= pointObservation )
                pointObservationRecord.save()

                serializer = serializers.PointObservationRecordSerializer(pointObservationRecord)

                return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            ## create new  pointObservation
            village = models.Village.objects.only('pk').get(pk=data['observation_village'])
            zone = models.Zone.objects.only('pk').get(pk=data['observation_zone'])
            work = models.Work.objects.only('pk').get(pk=data['observation_work'])
            secure = models.SecureGuard.objects.only('pk').get(pk=data['observation_secure'])
            pointObservation = models.PointObservation.objects.create(observation_village=village, observation_zone=zone, observation_work=work, observation_secure=secure, observation_date=data['observation_date'])
            pointObservation.save()

            ## create new PointObservationRecord
            pointPkList = models.Checkpoint.objects.filter(point_zone=data['observation_zone'],is_active=True,point_active=True).values_list('pk', flat=True)
            for pointPk in pointPkList: ## all point 
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=pointPk)
                pointObservationPointList = models.PointObservationPointList.objects.create(observation_pk=pointObservation, checkpoint_pk = checkpoint)
                pointObservationPointList.save()


            isExistPOR = models.PointObservationRecord.objects.filter(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk']).exists()
            if(isExistPOR==True):
                ## already have pointObservationRecord
                pointObservationRecord = models.PointObservationRecord.objects.only('pk').get(observation_pk=pointObservation, observation_timeslot=data['observation_timeslot'],checkpoint_pk = data['checkpoint_pk'])
                return Response({ "detail": 'already have this pointObservationRecord'},status=status.HTTP_200_OK)
            else:
                ## create new  pointObservationRecord
                checkpoint = models.Checkpoint.objects.only('pk').get(pk=data['checkpoint_pk'])
                pointObservationRecord = models.PointObservationRecord.objects.create(observation_checkin_time=data['observation_checkin_time'], observation_checkout_time=data['observation_checkout_time'],observation_timeslot=data['observation_timeslot'],checkpoint_pk = checkpoint, observation_pk= pointObservation )
                pointObservationRecord.save()

                serializer = serializers.PointObservationRecordSerializer(pointObservationRecord)

                return Response(serializer.data,status.HTTP_201_CREATED)