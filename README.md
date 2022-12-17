# JobReccer
A self-adaptive job recommendation system for candidates to find the best matching jobs. 

Environment Requirement:
Refer to the environment.txt file. 

Cold start (without data): 
1. In the project root directory, run $python ./scripts/rating.py, you will be asked to input job rating to start, be patient and finish your data inputs (This is very important for the system to function properly in later steps.)
2. After finishing initial data labeling, under the same project root directory, run $python ./scripts/resume_parser.py to parse the resumes into computer legible data formats. 
3. In the same directory, run $python ./scripts/pproducequery.py to generate query from parsed resume data. 
4. In the project root directory, run $python ./scripts/train_test_validation_generate.py to generate the datasets for further training and processing
5. In the project root directory, run $python run.py Please be patient as the initialization time for a new user can take 2-3 mins

Normal start:
Start with non-empty job_user_rating.csv:
In project root directory, run $python run.py Please be patient as the initialization time for a new user can take 2-3 mins...
Then follow the prompts on screen



