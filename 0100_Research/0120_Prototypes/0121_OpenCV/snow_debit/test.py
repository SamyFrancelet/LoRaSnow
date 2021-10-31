import csv

def csvTest():
    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

def main():
    l = [('Result_1', 'Result_2', 'Result_3', 'Result_4'), (1, 2, 3, 4), (5, 6, 7, 8)]
    cs = zip(*l)
    print(l)
    print(cs)

if __name__ == "__main__":
    main()
