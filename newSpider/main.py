from getOneBook import getBook
from getAuthorBooks import getAuthorBooks
from Author import Author
import time


def main():
    a1 = Author('米兰・昆德拉', 'https://m.xyyuedu.com/wgmz/milankundela/index.html')
    dic = getAuthorBooks(a1).getBooksUrl()
    AuthorBooks = getBook(dic)
    AuthorBooks.getBooks()


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time()

    print("用时{}s".format(end_time-start_time))

