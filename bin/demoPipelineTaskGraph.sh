pipetask -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i 'raw','calib','shared/ci_hsc' -o test/all qgraph --pipeline-dot ./allPipeline.dot  --qgraph-dot allGraph.dot \
-t isrTask.IsrTask:isr -C isr:$DEMO_HSC_PIPELINETASK_DIR/config/isr.py \
-t characterizeImage.CharacterizeImageTask:cit -C cit:$DEMO_HSC_PIPELINETASK_DIR/config/charImage.py \
-t calibrate.CalibrateTask:ct -C ct:$DEMO_HSC_PIPELINETASK_DIR/config/calibrate.py \

pipetask -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i 'shared/ci_hsc' -o test/all qgraph --pipeline-dot ./allPipelineCoadd.dot --qgraph-dot allGraphCoadd.dot \
-t makeCoaddTempExp.MakeWarpTask:mwt -C mwt:$DEMO_HSC_PIPELINETASK_DIR/config/makeWarp.py \
-t assembleCoadd.CompareWarpAssembleCoaddTask:cwact -C cwact:$DEMO_HSC_PIPELINETASK_DIR/config/compareWarpAssembleCoadd.py \

pipetask -b $CI_HSC_DIR/DATA/butler.yaml -p lsst.ip.isr -p lsst.pipe.tasks -i 'shared/ci_hsc' -o test/all qgraph --pipeline-dot ./allPipelineCoaddMeasure.dot --qgraph-dot allGraphCoaddMeasure.dot \
-t multiBand.DetectCoaddSourcesTask \
-t mergeDetections.MergeDetectionsTask:mdt -C mdt:$DEMO_HSC_PIPELINETASK_DIR/config/mergeDetections.py \
-t deblendCoaddSourcesPipeline.DeblendCoaddSourcesSingleTask \
-t multiBand.MeasureMergedCoaddSourcesTask:mmcst -C mmcst:$DEMO_HSC_PIPELINETASK_DIR/config/measureMerged.py \
-t mergeMeasurements.MergeMeasurementsTask:mmt -C mmt:$DEMO_HSC_PIPELINETASK_DIR/config/mergeCoaddMeasurements.py


