stardocker
==========

An extensible Starcluster launcher that can be easily configured to run docker applications.

The ultimate goal of the project is to be able to setup and run a potentially complex analysis pipeline
encapsulated in a docker container on an on-demand, automatically-configured cluster, such as StarCluster
in AWS. For example, I want to be able to type something like this:

```
$stardocker up pipeline --container dimenwarper/pipeline --volumes s3://bucket_with_data:/data/ s3://auxiliary_data:/aux/
$stardocker run pipeline
```

And have a StarCluster instance automatically configured and initiated and that will spawn workers that will execute 
the dimenwarper/pipeline docker container on data contained in bucket\_with\_data (which can be local, or s3, etc.)
and with auxiliary data (say, a reference genome for genome alignment tasks) in auxiliary_data.
