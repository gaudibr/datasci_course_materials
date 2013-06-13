register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar

raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-*' USING TextLoader as (line:chararray);

ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);

objects = group ntriples by (subject) PARALLEL 50;

count_by_object = foreach objects generate flatten($0), COUNT($1) as count PARALLEL 50;

group_count = group count_by_object by (count) PARALLEL 50;

count_by_count = foreach group_count generate flatten($0) as x, COUNT($1) as y PARALLEL 50;

store count_by_count into '/user/hadoop/example-results' using PigStorage();
