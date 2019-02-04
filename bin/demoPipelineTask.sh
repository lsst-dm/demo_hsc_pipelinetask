COLLECTION=test/all5

python $DEMO_HSC_PIPELINETASK_DIR/bin/ingestSkyMap.py $CI_HSC_DIR/DATA $COLLECTION
python $DEMO_HSC_PIPELINETASK_DIR/bin/ingestBrightObjectMask.py $CI_HSC_DIR/DATA $COLLECTION

pipetask -j 15 -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i 'raw','calib',ref/ps1_pv3_3pi_20170110,$COLLECTION -o $COLLECTION run \
-t isrTask.IsrTask:isr -C isr:$DEMO_HSC_PIPELINETASK_DIR/config/isr.py \
-t characterizeImage.CharacterizeImageTask:cit -C cit:$DEMO_HSC_PIPELINETASK_DIR/config/charImage.py \
-t calibrate.CalibrateTask:ct -C ct:$DEMO_HSC_PIPELINETASK_DIR/config/calibrate.py \

pipetask -d "Patch.patch = 69" -j 15 -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i $COLLECTION -o $(echo $COLLECTION)Coadd run \
-t makeCoaddTempExp.MakeWarpTask:mwt -C mwt:$DEMO_HSC_PIPELINETASK_DIR/config/makeWarp.py \
-t assembleCoadd.CompareWarpAssembleCoaddTask:cwact -C cwact:$DEMO_HSC_PIPELINETASK_DIR/config/compareWarpAssembleCoadd.py \

pipetask -d "Patch.patch = 69" -j 8 -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i $COLLECTION,$(echo $COLLECTION)Coadd -o $(echo $COLLECTION)CoaddMeas run \
-t multiBand.DetectCoaddSourcesTask \
-t mergeDetections.MergeDetectionsTask:mdt -C mdt:$DEMO_HSC_PIPELINETASK_DIR/config/mergeDetections.py \
-t deblendCoaddSourcesPipeline.DeblendCoaddSourcesSingleTask \
-t multiBand.MeasureMergedCoaddSourcesTask:mmcst -C mmcst:$DEMO_HSC_PIPELINETASK_DIR/config/measureMerged.py \
-t mergeMeasurements.MergeMeasurementsTask:mmt -C mmt:$DEMO_HSC_PIPELINETASK_DIR/config/mergeCoaddMeasurements.py
