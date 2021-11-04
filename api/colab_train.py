# input for model prediction
testdata=test_data=input_file.text[11000]
print(testdata)

# prediction
doc2 = nlp(testdata)
article_Categories=doc2.cats

#sorted article label based on probability
sorted_d = dict( sorted(article_Categories.items(), key=operator.itemgetter(1),reverse=True))
print(sorted(article_Categories, reverse=True))

# predicton output
print (testdata)
for k,v in sorted(article_Categories.items(), key=operator.itemgetter(1),reverse=True)[:10]:
  print (k,":",v)
