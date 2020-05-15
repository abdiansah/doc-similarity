from DocSimilarity import DocSimilarity

main = DocSimilarity()
threshold = 0.7

filenames = main.ekstrak_filename('./docs/', 0, 14)
data = main.ekstrak_pdf('./docs/', filenames)
main.cek_kemiripan(data, threshold)
print('\n')
main.tampilkan_hasil() 
