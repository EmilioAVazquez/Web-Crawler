from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import xml.etree.cElementTree as ET
import multiprocessing
import time

class Stack_Words(object):
    """
    The invariant of this data structure is that a word cannot be entered more than once.
    For this reason the data structure keeps a log of words that were entered in the past.
    Similarly, this stack cannot store the same word twice, only one should remain. The already
    stored data elements have lower precedence than the new incomming data. This is, if an already
    existing data element is push on the top of the stack, the element on the top will remain
    while the element at the bottom will be deleted. An element is permantely deleted when
    it's popped and thus will be passed to the log list.
    """
    #N: number of words stored in words
    #L: number of words stored in logged
    def __init__(self, list_words):
        """
        Use it to get the top elements of the stack.
        Input: an array of words
        Ouput: nothing
        Type:  initialize
        """
        self.words  = list_words[:]
        self.logged = []
        self.size   = len(self.words)

    def get(self, number = 1):
        """
        Use it to get the top elements of the stack.
        Input: number of elements at the top
        Ouput: array of top elements
        Type:  query
        """
        return self.words[self.size - number: ]

    def get_stack(self):
        """
        Use it to get all the stack.
        Input: Nothing
        Ouput: array of stack
        Type:  query
        """
        return self.words

    def pop(self, number = 1):
        """
        Use it to pop the top elements of the stack.
        Input: number of elements at the top
        Ouput: Nothing
        Type:  Mutator
        """
        self.logged.extend(self.words[self.size - number: ])
        for n in range(number):
            self.words.pop()
        self.size   = len(self.words)

    def push(self, array):#this could also be implemented with single objects
        """
        Use it to set new elements at the top of the stack
        Input: array of elements to set on top of the stack
        Ouput: Nothing
        Type:  Mutator
        """
        array = self.del_dup_input(array)
        array = self.del_logged(array)
        self.del_dupl(array)#mutator
        self.words.extend(array)
        #self.check()#will check for cuplciates in log and words
        self.size   = len(self.words)

    def del_dupl(self, array):#Best case complexity: assuming N >> len(array) => O(N)
        for e in array:
            if e in self.words:
                self.words.remove(e)

    def del_logged(self, array):#Best case complexity: assuming L >> len(array) => O(L)
        temp = []
        for e in array:
            if e not in self.logged:
                temp.append(e)
        return temp

    def del_dup_input(self,array):
        temp = []
        for e in array:
            if not e in temp:
                temp.append(e)
        return temp

    def backup(self, path1, path2):
        file1 = open( path1, "w", encoding= "utf-8" )
        file2 = open( path2, "w", encoding= "utf-8" )
        for w in self.words:
            file1.write(w + "\n")
        for w in self.logged:
            file2.write(w + "\n")
        file1.close()
        file2.close()

    def load_logged(self, path):
        file = open( path, "r", encoding= "utf-8" )
        for line in file:
            self.logged.append(line.strip())
        file.close()

    def load_words(self, path):
        file = open( path, "r", encoding= "utf-8" )
        for line in file:
            self.words.append(line.strip())
        file.close()

    def check(self):
        for word in self.logged:
            if word in  self.words:
                while word in self.words:
                    self.words.remove(word)


#Global variables
path_to_extension   = r'/home/emiliovazquez/Web-Crawler/Webdriver/3.31.2_0'
path_to_driver1     =  "/home/emiliovazquez/Web-Crawler/Webdriver/chromedriver1"
path_to_driver2     =  "/home/emiliovazquez/Web-Crawler/Webdriver/chromedriver2"
path_to_driver3     =  "/home/emiliovazquez/Web-Crawler/Webdriver/chromedriver3"
path_to_driver4     =  "/home/emiliovazquez/Web-Crawler/Webdriver/chromedriver4"
# instantiate a chrome options object so you can set the size and headless preference
chrome_options      = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)#Adblocker
chrome_options.add_argument("--headless")#Headless
chrome_options.add_argument("--window-size=1920x1080")
browser1            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver1 , port=9515)
browser2            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver2 , port=9514)
browser3            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver3 , port=9513)
browser4            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver4 , port=9512)

def job(browser_number, word, queue):

    if   browser_number == 1:
        browser =  browser1
    elif browser_number  == 2:
        browser =  browser2
    elif browser_number  == 3:
        browser =  browser3
    elif browser_number  == 4:
        browser =  browser4

    browser.execute(Command.SET_TIMEOUTS, {'ms': float(my_timeout_secs * 1000), 'type': 'page load'})

    url      = "http://www.elmundo.es/diccionarios/"#URL to attack
    #print (input_words.get()[0].encode('ascii', 'ignore'))#print(input_words.get()[0].encode('latin1').decode('utf8'))
    #print (word.encode('ascii', 'ignore'))#print(word.encode('latin1').decode('utf8'))

    browser.get(url) #navigate to the page

    selection    = browser.find_element_by_xpath("//input[@name='diccionario' and @value='2']")
    selection.click()# click radio button

    text_area    = browser.find_element_by_xpath("//input[@name='busca' and @type='text']")
    text_area.send_keys(word)# type text

    submit_button= browser.find_elements_by_xpath("//input[@name='submit' and @class='buscar']")[0]
    submit_button.click()

    name         = browser.find_element_by_xpath("//div[@class='resultado']")

    title        = name.find_elements_by_tag_name('h2')
    synonyms     = name.find_elements_by_tag_name('li')

    head = []
    body = []
    if len(title) != 0:#this is the word
        head.append(title[0].text)
    if len(synonyms) != 0:#these are the synonyms
        for s in synonyms:
            body.append(s.text)
    queue.put([[head,body]])

def retrive_fromfile_array(path):
    file                = open(path, "r", encoding= "utf-8")
    array = []
    for line in file:
        array.append(line.strip())#strip() or get fucked!
    file.close()
    return array

def update_synonyms_Tree(queue, xml_tree):#unefficent as fuck!
    array = []
    while queue.empty() is False:
        for result in queue.get():
            if len(result[0]) != 0:#this is the word
                search = ET.SubElement(xml_tree, "word")
                ET.SubElement(search, "title" ).text = result[0][0]
            if len(result[1]) != 0:#these are the synonyms
                array.extend(result[1])
                for synonym in result[1]:
                    ET.SubElement(search, "syn").text = synonym
    return array

def reset_browsers():
    global browser1
    global browser2
    global browser3
    global browser4

    browser1.quit()
    browser2.quit()
    browser3.quit()
    browser4.quit()

    browser1            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver1 , port=9515)
    browser2            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver2 , port=9514)
    browser3            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver3 , port=9513)
    browser4            = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_driver4 , port=9512)

if __name__ == '__main__':
    #Data paths: input(words), output(xml file path and xml tree)
    path_to_words       = "/home/emiliovazquez/Web-Crawler/Input_Files/listado-general.txt"
    path_to_notlogged   = "/home/emiliovazquez/Web-Crawler/Input_Files/notlogged.txt"
    path_to_logged      = "/home/emiliovazquez/Web-Crawler/Input_Files/logged.txt"
    path_to_backupnl    = "/home/emiliovazquez/Web-Crawler/Input_Files/notlogged1.txt"
    path_to_backupl     = "/home/emiliovazquez/Web-Crawler/Input_Files/logged1.txt"
    path_to_seeds       = "/home/emiliovazquez/Web-Crawler/Input_Files/seeds.txt"
    path_to_synonymsDB  = "/home/emiliovazquez/Web-Crawler/Input_Files/synWords1.xml"
    synonyms_xmlTree    = ET.Element("data")

    #User update interface
    flag = True
    downloaded = 0
    ini_time = time.time()


    input_words = Stack_Words([])
    input_words.load_words(path_to_notlogged)
    input_words.load_logged(path_to_logged)
    input_words.push(retrive_fromfile_array(path_to_seeds))
    queue = multiprocessing.Queue()#queue used for communication among the browsers
    number_browsers = 4#may chaneg dependingon the number of parallel browsers
    browsers = [1,2,3,4]

    int_time = time.time()

    while flag:
        words_to_search = input_words.get(number_browsers)
        all_processes = [multiprocessing.Process(target=job, args = (browsers[i],words_to_search[i],queue)) for i in range(number_browsers)]
        for p in all_processes:
            p.start()
        for p in all_processes:
            p.join()
        input_words.pop(number_browsers)#marked as visited
        input_words.push(update_synonyms_Tree(queue, synonyms_xmlTree))

        downloaded = downloaded + number_browsers

        if downloaded%(60000) == 0:
            print(downloaded)
            break

        if downloaded%(200) == 0:
            print('Number of words dondownloaded: ', downloaded,' Speed: ', (time.time() - ini_time)/downloaded, 'sec/wrd', ' Last words len ', input_words.get()[0], "  ", time.time() - ini_time)

        if downloaded%(800) == 0:
            reset_browsers()


    input_words.backup(path_to_backupnl, path_to_backupl)
    tree = ET.ElementTree(synonyms_xmlTree)
    tree.write(path_to_synonymsDB)
    browser1.quit()
    browser2.quit()
    browser3.quit()
    browser4.quit()
    #synWords.close()
    print("Finished!")
