from DocSimilarity import DocSimilarity

main = DocSimilarity()
threshold = 0.7

data = main.ekstrak_csv('docs.csv', 0, 1) # 2: kolom-2, 3: kolom-3
main.cek_kemiripan(data, threshold)
print('\n')
main.tampilkan_hasil()