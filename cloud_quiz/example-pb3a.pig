register s3n://uw-cse-344-oregon.aws.amazon.com/myudfs.jar


raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/cse344-test-file' USING TextLoader as (line:chararray);
ntriples = foreach raw generate FLATTEN(myudfs.RDFSplit3(line)) as (subject:chararray,predicate:chararray,object:chararray);


filter1 = FILTER ntriples BY subject matches '.*business.*';
filter2 = FOREACH filter1 GENERATE subject as subject2, predicate as predicate2, object as object2;

join1 = JOIN filter1 BY subject, filter2 BY subject2;

results = DISTINCT join1;


store results into '/user/hadoop/example-results' using PigStorage();

-- store count_by_count into '/user/hadoop/example-results' using PigStorage();
-- load the test file into Pig
-- later you will load to other files, example:
-- raw = LOAD 's3n://uw-cse-344-oregon.aws.amazon.com/btc-2010-chunk-000' USING TextLoader as (line:chararray); 

-- parse each line into ntriples
-- group the n-triples by object column
-- objects = group ntriples by (subject) PARALLEL 50;

-- flatten the objects out (because group by produces a tuple of each object
-- in the first column, and we want each object ot be a string, not a tuple),
-- and count the number of tuples associated with each object
-- count_by_object = foreach objects generate flatten($0), COUNT($1) as count PARALLEL 50;

-- group_count = group count_by_object by (count) PARALLEL 50;

-- count_by_count = foreach group_count generate flatten($0) as x, COUNT($1) as y parallel 50;

-- order the resulting tuples by their count in descending order
-- count_by_object_ordered = order count_by_object by (count)  PARALLEL 50;

-- store the results in the folder /user/hadoop/example-results
-- Alternatively, you can store the results in S3, see instructions:
-- store count_by_object_ordered into 's3n://superman/example-results';
