#Grace Morris and Sadie Rollings
#This program models how mutation affects genetic distance over many generations.

import random
import xlsxwriter

def main():
    workbook = xlsxwriter.Workbook('project2.xlsx')
    worksheet = workbook.add_worksheet()
    N = int(input("Please enter the number of individuals per generation: ")) #N is the number of individuals per generation
    if (N < 0): #validate input
        print("Enter a positive number.")
        exit(1)
    L = int(input("Please enter the number of nucelotides in each individual's genetic sequence: ")) #L is the length of the sequence
    if (L < 0): #validate input
        print("Enter a positive number.")
        exit(1)
    mu = float(input("Please enter the rate of mutation: ")) #mu is the rate of mutation
    if (mu < 0 or mu > 1): #validate input
        print("Enter a number between 0 and 1.")
        exit(1)
    G = int(input("Please enter the number of total generations: ")) #G is the total number of generations
    if (G < 0): #validate input
        print("Enter a positive number.")
        exit(1)
    g = int(input("Please enter the generation number that you would like the speciation event to occur: ")) #g is the time when the speciation event should occur
    if (g < 0): #validate input
        print("Enter a positive number.")
        exit(1)
    generation = [] #list to hold the entire generation of individuals
    individual = [] #list to hold the nucleotide sequence of an individual
    genetic_distance_list = [] #list to hold the values of genetic distance for each generation
    genetic_distance_list.append(0.0) #no genetic distance for Gen 0
    i = 0
    while(i < N): #loop to initialize the beginning generation to all "A" nucleotides
        i = int(i)
        j = 0
        while(j < L):
            individual.append('A')
            j = j+1
        generation.append(individual)
        individual = []
        i = i + 1

    gen_dist_a = [] #list to hold the first break-off geneneration's genetic distance
    gen_dist_b = [] #list to hold the second break-off generation's genetic distance
    generation_index = 0
    i = 0
    populationA = [] #list to hold the first break-off generation
    populationB = [] #list to hold the second break-off generation
    split = False
    first = True
    while (generation_index <= G): #while less than the total # of generations
        if (generation_index < g): #if we haven't reached the speciation event
            generation = reproduce(generation, N, L, mu)
            genetic_distance_list = genetic_distance(N, L, generation, genetic_distance_list)
        else: #else if we have reached the speciation event
            split = True
            break
        generation_index = generation_index + 1

    while (i < N/2): #initialize populationA
        populationA.append(generation[i])
        i = i + 1
    i = int(N/2)
    while (i < N): #initialize populationB
        populationB.append(generation[i])
        i = i+1

    while (generation_index < G): #while less than the total number of generations
        populationA = reproduce(populationA, N/2, L, mu)
        populationB = reproduce(populationB, N/2, L, mu)
        if (first): #the first time we want to make sure the genetic distance of the past populations is added to the list
            first = False
            gen_dist_a = genetic_distance_list + genetic_distance(N/2, L, populationA, gen_dist_a)        
            gen_dist_b = genetic_distance_list + genetic_distance(N/2, L, populationB, gen_dist_b)
        else:
            gen_dist_a = genetic_distance(N/2, L, populationA, gen_dist_a)        
            gen_dist_b = genetic_distance(N/2, L, populationB, gen_dist_b)
        generation_index = generation_index + 1


    worksheet.write('A1', 'Generation')
    worksheet.write('B1', 'Population A')
    worksheet.write('C1', 'Population B')
    excel_index = 2
    i = 0
    if (split): #output
        while (i <= G): #write to excel
            worksheet.write('A'+ str(excel_index), i)
            worksheet.write('B'+ str(excel_index), gen_dist_a[i])
            worksheet.write('C'+ str(excel_index), gen_dist_b[i])
            i = i+1
            excel_index = excel_index + 1
        print("Generation A: ")
        print_gen(populationA)
        print_distance(gen_dist_a)
        print("\nGeneration B: ")
        print_gen(populationB)
        print_distance(gen_dist_b)
    else:
        while (i <= G):
            worksheet.write('A'+ str(excel_index), i)
            worksheet.write('B'+ str(excel_index), genetic_distance_list[i])
            worksheet.write('C'+ str(excel_index), genetic_distance_list[i])
            i = i+1
            excel_index = excel_index + 1
        print_gen(generation)
        print_distance(genetic_distance_list)
    workbook.close()

#This function creates a new generation based off mutating the parent's DNA
#Parameters: generation, the list containing every individual and their sequence
# N, the total number of individuals
# L, the length of their nucleotide sequences
# mu, the rate of mutation
#Returns: the list containing the new generation
def reproduce(generation, N, L, mu):
    i = 0
    j = 0
    while (i < N):
        j = 0
        while (j < L):
            nucleotide = generation[i][j]
            nucleotide = mutate(nucleotide, mu)
            generation[i][j] = nucleotide
            j = j+1
        i = i + 1
    return generation

#This function uses mu and random chance to determine whether an individual nucleotide will mutate
#Parameters: nucleotide, the nucleotide to mutate
# mu, the rate of mutation
#Returns: nucleotide, the mutated nucleotide
def mutate(nucleotide, mu):
    if random.random() <= mu: #determines whether mutation will occur
        if random.random() <= (1/3): #1/3 chance of transversion
            if nucleotide == 'A' or nucleotide == 'G':
                nucleotide = random.choice(list('TC'))
            elif nucleotide == 'T' or nucleotide == 'C':
                nucleotide = random.choice(list('AG'))
        else:
            if nucleotide == 'A': nucleotide = 'G'
            elif nucleotide == 'G': nucleotide = 'A'
            elif nucleotide == 'T': nucleotide = 'C'
            elif nucleotide == 'C': nucleotide = 'T'
    return nucleotide

#This function calculates the genetic distance of each generation by adding up all the differences between pairs and taking the average.
#Paramters: N, the total number of individuals
#L, the length of the nucleotide sequence
#generation, the list containing all of the individuals of the current generation
#genetic_distance_list, a list containing the genetic distance averages of every generation
#Returns: genetic_distance_list, the modified list containing the average genetic distances for every generation
def genetic_distance(N, L, generation, genetic_distance_list):
    differences = 0
    indiv_index = 0
    total = 0
    while (indiv_index < N):
        individual1 = generation[indiv_index]
        i = indiv_index + 1
        while (i < N):
            j = 0
            while (j < L):
                individual2 = generation[i]
                if (individual1[j] != individual2[j]):
                    differences = differences + 1
                j = j+1
            total += differences
            differences = 0
            i = i + 1
        indiv_index = indiv_index + 1
    gen_distance = (total/N)/L
    genetic_distance_list.append(gen_distance)
    return genetic_distance_list

#This function exists purely to format output without making the main() function messy
#It prints the list of nucleotides as a string for readability
#Parameters: generation, the group of individuals to output
def print_gen(generation):
    output_index = 0
    genotype = ''
    while (output_index < len(generation)):
        i = 0
        while (i < len(generation[output_index])):
            genotype = genotype + generation[output_index][i]
            i = i + 1
        print(genotype)
        genotype = ''
        output_index = output_index + 1

#This function is to print the genetic distance list in a readable way
#Parameters: genetic_distance_list, the list containing the average genetic distance for each generation
def print_distance(genetic_distance_list):
    output_index = 0
    while (output_index < len(genetic_distance_list)):
        print("Generation ", output_index, ": ", genetic_distance_list[output_index])
        output_index = output_index + 1

if __name__ == "__main__": #this calls main in Python
    main()