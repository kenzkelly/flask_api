import csv
import spacy


class Predictor():

    def __init__(self, o_value, c_value, e_value, a_value, n_value):
        self.o_value = o_value
        self.c_value = c_value 
        self.e_value = e_value 
        self.a_value = a_value 
        self.n_value = n_value 

        self.nlp = spacy.load("en_core_web_lg")

        # Define the descriptions
        self.oceans = [
            {0 : 'Closed', 1: 'Conservative', 2 : 'Cautious', 3 : 'Curious', 4 : 'Creative', 5 : 'Innovative', 6 : 'Visionary', 7 : 'Original', 8 : 'Imaginative', 9 : 'Unorthodox'},
            {0 : 'Disorganized', 1 : 'Unstructured', 2 : 'Easy-going', 3 : 'Average', 4 : 'Organized', 5 : 'Responsible', 6 : 'Disciplined', 7 : 'Conscientious', 8 : 'Highly-organized', 9 : 'Perfectionist'},
            {0 : 'Reserved', 1 : 'Quiet', 2 : 'Balanced', 3 : 'Average', 4 : 'Outgoing', 5 : 'Sociable', 6 : 'Gregarious', 7 : 'Highly-extraverted', 8 : 'Very-outgoing', 9 : 'Extremely-extroverted'},
            {0 : 'Critical', 1 : 'Stubborn', 2 : 'Independent', 3 : 'Average', 4 : 'Friendly', 5 : 'Compassionate', 6 : 'Warm', 7 : 'Very-agreeable', 8 : 'Extremely-considerate', 9 : 'Selfless'},
            {0 : 'Stable', 1 : 'Relaxed', 2 : 'Moderate', 3 : 'Anxious', 4 : 'Sensitive', 5 : 'Worried', 6 : 'Reactive', 7 : 'Very-sensitive', 8 : 'Extremely-neurotic', 9 : 'Overwhelmingly-anxious'}
        ]

    #computes the average similarity of a job description
    def get_avg_similarity(self, description, base_token): 
        desc_nlp = self.nlp(description)

        total = 0

        for token in desc_nlp: 
            total += token.similarity(base_token)
        
        return total/len(description.split())

    #for one job description, computes the total similarity between each OCEANS value
    def total_ocean_similarity(self, description): 
        total_similarity = 0

        #calculating o-similarity
        o_similarity_base = self.nlp(self.oceans[0].get(self.o_value))
        total_similarity += self.get_avg_similarity(description, o_similarity_base)

        #calculating c-similarity
        c_similarity_base = self.nlp(self.oceans[1].get(self.c_value))
        total_similarity += self.get_avg_similarity(description, c_similarity_base)

        #calculating e-similarity
        e_similarity_base = self.nlp(self.oceans[2].get(self.e_value))
        total_similarity += self.get_avg_similarity(description, e_similarity_base)

        #calculating a-similarity
        a_similarity_base = self.nlp(self.oceans[3].get(self.a_value))
        total_similarity += self.get_avg_similarity(description, a_similarity_base)

        #calculating n-similarity
        n_similarity_base = self.nlp(self.oceans[4].get(self.n_value))
        total_similarity += self.get_avg_similarity(description, n_similarity_base)

        return total_similarity

    #goes through the job/description file and generates similarity for each 
    def compute_similarity(self, file_name): 
        #will keep track of the job,description pair and similarity rating 
        top_5 = [{0:'0'}, {0:'0'}, {0:'0'}, {0:'0'}, {0:'0'}]

        #read through 
        with open(file_name, 'r') as file: 
            reader = csv.reader(file)

            for row in reader:
                if reader.line_num % 2 != 0:
                    description = row[1]
                    similarity_score = self.total_ocean_similarity(description)

                    if similarity_score > list(top_5[4].keys())[0]: 
                        i = 4 
                        while i >= 0 and similarity_score > list(top_5[i].keys())[0]:
                            i = i - 1
                        
                        top_5.insert(i+1, {similarity_score : row[0]})
                        del top_5[5]
        
        return top_5
                



