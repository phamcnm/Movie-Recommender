# Movie Recommender

## Co-Authors
  Yuting Su and Minh Pham
  
## Summary

  We used Wikipedia API(code in `get_movies.py`) to collect 2081 acticles fetched from Lists of American Films between 2000 to 2020. Each article consists of a short summary, a plot, and a list of casts. We then used Doc2Vec model to generate frequency matrix of words that appear in each article. The general idea of Doc2Vec is to create a vector representation of each article that maintains 'points' on 'important' words that can be used to come up with the similarity between two articles (articles that have similar words will likely be realted). We also used named entity recognition to find people's names and/or palces to display on the `Keywords` section and used dependency parsing around those keywords to comeup with `Rephrased Summaries`. We also used markov_chain on thousands of movie reviews in `clean_review.txt` to generate reviews and used sentimental analysis to come up with the rating based on the generated reviews.
  
 #### Final product: `search.py`
   The `search.py` takes in a string on the input and uses Wikipedia API to get a wiki article of a given movie name. It then uses the doc2vec model that are stored in `./bot_dependencies/doc2vec.model` to generate a vector from the fetched article. After that, it gets top five 'most similar movies' by comparing the vector with other vectors in the matrix(generated from 2081 articles) stored in `./bot_dependencies/matrix.dat` by calculating cosine similarity scores. The top 5 articles then go through dependency parsing, markov_chain text generation, and sentimental analysis to create the end result.
  
## Sample Output from Commandline

### Entering "Hulk" as an input

    Enter a topic: Hulk         
    ======================================================================================================================================================
                                                                         0. Hulk 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                                         Match: 9.23/10                                         Rating: 6.17/10                                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Keywords: Bruce | Ross | Lee | France | Schamus | Talbot                                                    
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Rephrased Summaries: Hensleigh wrote before Lee.

                                           who make revert.

                                           Talbot attacks about lab.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Reviews: Return to the humdrum again. A kitchen sink world of bakeries, and hairdressers.                  

                               Having been a marine, I can' t really say what I feel this.                   

                               If you are not my father," such as the superb janus and.                      

    ======================================================================================================================================================

    ======================================================================================================================================================
                                                                      1. Spider-Man 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                                         Match: 6.64/10                                         Rating: 5.79/10                                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                    Keywords: Spider-Man | Peter | Norman | New York City | the United States | Los Angeles                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                    Rephrased Summaries: it is some mysterious stuff.

                                         Peter dodges attack.

                                         Man is some mysterious stuff.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
                    Reviews: Super troopers was an instant classic. Club dread, while disappointing to many.                   

                             I waited for this movie and some interesting plot. And I loved the end.                  

                             This movie was bad. I am in the right place as he examines this.                  

    ======================================================================================================================================================

    ======================================================================================================================================================
                                                                       2. Glass 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                                         Match: 6.55/10                                         Rating: 4.92/10                                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Keywords: Glass | Split | Kevin | the United States | Dunn | Canada                                         
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Rephrased Summaries: mother try some mysterious stuff.

                                           creator sees at turn.

                                           Elijah escapes cell.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Reviews: My first exposure to the templarios& not a good job. Marion davies.                               

                               Had it with the one who knows what' s going on?.                              

                               My roommate and I have to go watch it! this could have been.                  

    ======================================================================================================================================================

    ======================================================================================================================================================
                                                                      3. Unbreakable 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                                         Match: 6.36/10                                         Rating: 5.64/10                                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Keywords: David | Shyamalan | Glass | Split | the United States | Shyamalan                                 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Rephrased Summaries: who bump into Dunn.

                                           who bump into Dunn.

                                           Shyamalan began After success.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Reviews: Despite having an absolutely horrid script( more about that later) and the color.                  

                               A found tape about 3? guys having fun torturing a woman in several inhuman.                  

                               The premise of the movie... the plot is really simple. Stiller.                  

    ======================================================================================================================================================

    ======================================================================================================================================================
                                                                         4. X-Men 
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                                         Match: 6.33/10                                         Rating: 5.21/10                                     
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Keywords: Wolverine | Kinberg | Logan | Canada | Kinberg | Vancouver                                        
    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Rephrased Summaries: Mutants concluding in 2020.

                                           photography began in March.

                                           Logan meet In 2029.

    ------------------------------------------------------------------------------------------------------------------------------------------------------
                      Reviews: I have seen them been handled better in several other films. Ms. Gai.                             

                               Nicholas walker is paul, the local town reverand who' s seduced by a.                  

                               I just got this video used and I was personally routing for the villain to.                  

    ======================================================================================================================================================

    Do you want to see the full spoliers for all 5 movies? [yes/no]: yes


    ======================================================================================================================================================
                                                                         0. Hulk 
    ------------------------------------------------------------------------------------------------------------------------------------------------------

                      Full Summaries: Hensleigh, John Turman, Michael France, Zak Penn (who would later write The Incredible Hulk), 
                                      J. Abrams, Michael Tolkin, David Hayter, Scott Alexander, and Larry Karaszewski wrote more 
                                      before Ang Lee and James Schamus' involvement. 

                                      Jennifer Connelly as Betty Ross:Bruce's ex-girlfriend and colleague, General Ross's 
                                      daughter, and possibly the only one who can make the Hulk revert into Bruce. 

                                      Talbot attacks Bruce about the lab; Bruce transforms and injures Talbot and Ross's MPs. 

    ======================================================================================================================================================
    ======================================================================================================================================================
                                                                      1. Spider-Man 
    ------------------------------------------------------------------------------------------------------------------------------------------------------

                      Full Summaries: Directed by Sam Raimi from a screenplay by David Koepp, it is the first installment in the 
                                      trilogy, and stars Tobey Maguire as the title character, alongside Willem Dafoe, Kirsten 
                                      James Franco, Cliff Robertson, and Rosemary Harris. 

                                      Warned by his spider sense, Peter dodges the attack and the glider fatally impales Norman, who 
                                      Peter not to reveal his identity as the Goblin to Harry before dying. 

                                      Spider-Man is a 2002 American superhero film based on the Marvel Comics character of the same 


    ======================================================================================================================================================
    ======================================================================================================================================================
                                                                         2. Glass 
    ------------------------------------------------------------------------------------------------------------------------------------------------------

                      Full Summaries: Elijah's mother Mrs. Price, Joseph Dunn, and Casey Cooke, a victim who survived Kevin/the 
                                      captivity, try and fail to convince Staple superhumans are real. 

                                      Audiences polled by CinemaScore gave the film an average grade of "B" on an A+ to F scale, down 
                                      Split's "B+" but up from Unbreakable's "C", while those at PostTrak gave it an overall positive 
                                      of 70% and a "definite recommend" of 49%.David Ehrlich of IndieWire gave the film a "C−" and 
                                      it the biggest disappointment of Shyamalan's career: "The trouble with Glass isn't that its 
                                      sees his own reflection at every turn, or that he goes so far out of his way to contort the film into 
                                      clear parable for the many stages of his turbulent career; the trouble with Glass is that its 
                                      intriguing meta-textual narrative is so much richer and more compelling than the asinine 
                                      that Shyamalan tells on its surface. 

                                      That night, Elijah escapes his cell to conduct research on Kevin before visiting him and 
                                      him he feigned his sedated state and plans to escape the institute but requires one of Kevin's 
                                      Beast—to help him. 

    ======================================================================================================================================================
    ======================================================================================================================================================
                                                                      3. Unbreakable 
    ------------------------------------------------------------------------------------------------------------------------------------------------------

                      Full Summaries: BoyDianne Cotten Murphy as Woman Walking ByIn October 2018, M. Night Shyamalan confirmed a fan 
                                      that "Five-Year-Old Boy" and "Woman Walking By" who bump into David Dunn outside a stadium are 
                                      versions of Kevin Wendell Crumb and Penelope Crumb from Split, confirmed in the 2019 film 


                                      BoyDianne Cotten Murphy as Woman Walking ByIn October 2018, M. Night Shyamalan confirmed a fan 
                                      that "Five-Year-Old Boy" and "Woman Walking By" who bump into David Dunn outside a stadium are 
                                      versions of Kevin Wendell Crumb and Penelope Crumb from Split, confirmed in the 2019 film 


                                      After the financial and critical success of Split, Shyamalan immediately began working on a 
                                      film, titled Glass, which was released January 18, 2019, thus making Unbreakable the first 
                                      in the Unbreakable film series. 

    ======================================================================================================================================================
    ======================================================================================================================================================
                                                                         4. X-Men 
    ------------------------------------------------------------------------------------------------------------------------------------------------------

                      Full Summaries: After each film outgrossed its predecessor, several spin-off films were released, including 
                                      Wolverine films (2009–2017), four X-Men: Beginnings films (2011–2019), and two Deadpool 
                                      (2016–2018), with The New Mutants concluding the series in 2020, after a 20-year-long run. 

                                      Principal photography began in March 2015 in Vancouver, Canada, and ended in May. 

                                      In 2029, Logan and Charles Xavier meet a young girl named Laura, a test-tube daughter of 
                                      who is being hunted by the Reavers led by Donald Pierce. 

    ======================================================================================================================================================
