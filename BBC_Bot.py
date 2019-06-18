from selenium import webdriver
import time
import os
import shutil

siteadi = 'XXX.com' #parameter 1 : WORDPRESS website name
siteProtokol = 'https://'
kullanici_adi = 'USERNAME'#parameter 2 : WORDPRESS ADMIN username
password = 'PASSWORD'#parameter 3 : WP ADMIN password
newsSelectFirst = 'BBC' #parameter 4 : There may be multiple news sites in the same folder. Specifies the path on code line 19
driverPath = 'geckodriver.exe' # ChromeDriver or geckoDriver Path
customerPath ="C:\\Users\\Administrator\\Desktop\\Musteriler\\FurkanTurkan\\2What_com\\" # comparison folder

# The folder structure is given in the description section of github

oldumu = 0
try:

    if newsSelectFirst:
        newsSelectFirstPath = "C:/Users/Administrator/Desktop/Haberler/"+newsSelectFirst+"_News/" #folder with all news
        files = os.listdir(newsSelectFirstPath) # news folders assigned to files variable
        i = 0
        while oldumu < 1:
            try:
                ad  = files[i]
                src = newsSelectFirstPath+ad# folder with all news
                dst = customerPath+"Published/"+ad#Hedef ayarla

                # move to published folder if it is not in the published folder and copied to content folder
                # if the folder already exists in the "published" folder, it is skipped.
                # content folder >>  the folder to be processed is copied to the "content" folder

                if not os.path.exists(dst):
                    shutil.copytree(src,dst)#TAŞI
                    print("copied to Published")
                    dstt = customerPath+"Contents/"+ad
                    shutil.copytree(dst,dstt)#TAŞI
                    print("copied to Content")
                    i +=1
                    oldumu +=1
                    print(oldumu)
                else:
                    i +=1
                    print("Dosya Atlandi")
            except:
                break

        # Open "content.txt" in the "content" folder and split with <-->
        files = os.listdir(customerPath+"Contents/")
        for content in zip(range(1),files):
            newContent = open(customerPath+"Contents/"+content[1]+"/Content.txt",encoding="utf8")
            newContent = newContent.read()
            newContent = newContent.split("<--->")
            #0 title
            #1 Content
            #2 Yoast META
            #3 Keyword
            #4 Tags
            #5 Category
            #6 IMG Alt
            try:
                content_Title      = newContent[0]
                content_Content    = newContent[1]
                content_YoastMeta  = newContent[2]
                content_Keyword    = newContent[3]
                content_Tags       = newContent[4]
                content_Category   = newContent[5]
                content_ImgAlt     = newContent[6]
            except:
                print("line 53 try except")
                exit()


            #selenium

            browser = webdriver.Firefox()
            browser.get(siteProtokol+siteadi+'/wp-admin') #login screen
            browser.maximize_window() #make full screen

            time.sleep(1) #wait

            #User Login
            browser.find_element_by_id('user_login').send_keys(kullanici_adi) #fill username
            browser.find_element_by_id('user_pass').send_keys(password) #fill password
            browser.find_element_by_id('wp-submit').click()# click login button


            time.sleep(2)

            # go to new post screen
            browser.get(siteProtokol+siteadi+'/wp-admin/post-new.php')

            # set category

            test = browser.find_element_by_xpath('//*[@id="in-category-1"]')
            test.click()
            test2 = browser.find_element_by_xpath('//*[@id="in-category-613"]')
            test2.click()

            #Add Title
            sel_baslik = browser.find_element_by_id('title')
            sel_baslik.send_keys(content_Title)

            #Add Content
            metin_gec = browser.find_element_by_xpath('//*[@id="content-html"]')
            metin_gec.click()
            kod_gecis = browser.find_element_by_xpath('//*[@id="content"]')
            kod_gecis.send_keys(content_Content)

            time.sleep(1)#Bekle

            #spinner OPTIONAL
            # rewrite = browser.find_element_by_xpath('//*[@id="wp-auto-spinner-post-rewrite"]')
            # time.sleep(3)
            # rewrite.click()
            # time.sleep(2)#Bekle
            # sendeditor= browser.find_element_by_xpath('//*[@id="wp-auto-spinner-stoeditor"]')
            # sendeditor.click()



            #Add Tags
            sel_etiket = browser.find_element_by_id('new-tag-post_tag')
            sel_etiket.send_keys(content_Tags+siteadi)

            time.sleep(1)
            ekle_button = browser.find_element_by_xpath('//*[@id="post_tag"]/div/div[2]/input[2]')
            ekle_button.click()

            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')

            #Add SEO
            sel_seo = browser.find_element_by_id('yoast-seo-analysis-collapsible-metabox')
            sel_seo.click()
            sel_keyword = browser.find_element_by_id('focus-keyword-input')
            sel_keyword.send_keys(content_Keyword)
            sel_kod_parca = browser.find_element_by_xpath('//*[@id="wpseo-metabox-root"]/div[2]/div/div/section/div/button')

            sel_kod_parca.click()
            time.sleep(2)#Bekle
            browser.find_element_by_xpath('//*[@id="snippet-editor-field-description"]').click()
            time.sleep(2)#Bekle
            browser.find_element_by_xpath('//*[@id="snippet-editor-field-description"]').send_keys(content_YoastMeta)
            time.sleep(1)#Bekle

            #Add Media
            browser.execute_script('window.scrollTo(0,450)')
            sel_ortam = browser.find_element_by_xpath('//*[@id="set-post-thumbnail"]')
            sel_ortam.click()
            sel_ortam_ekle = browser.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[3]/div/a[1]')
            sel_ortam_ekle.click()

            time.sleep(1)

            sel_ekle_button = browser.find_element_by_xpath("//*[starts-with(@id,'html5_')]//self::input")


            # when I was pulling the news I did their names like this: contentkeyword + str (i) example : car1, car2, car3
            content_ImgAlt = content_ImgAlt.split("<-->")
            for i in range(len(content_ImgAlt)-1):
                print(customerPath+"Contents/"+ad+"/"+content_Keyword+str(i)+ ".jpg")
                sel_ekle_button.send_keys(customerPath+"Contents\\"+ad+"\\"+content_Keyword+str(i)+ ".jpg") # upload wordpress gallery



            time.sleep(12) # wait for upload

            # set image alternative text, subtitle ...
            sel_alternatif_metin = browser.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[3]/div[2]/label[4]/input')
            sel_alternatif_metin.send_keys(content_ImgAlt[0])
            sel_altyazi = browser.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[3]/div[2]/label[3]/textarea')
            sel_altyazi.send_keys(content_ImgAlt[0])
            sel_tanim = browser.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[3]/div[2]/label[5]/textarea')
            sel_tanim.send_keys(content_ImgAlt[0])
            sel_belirle = browser.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[5]/div/div[2]/button')
            sel_belirle.click()
            time.sleep(1)
            # set author
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            yazar = browser.find_element_by_xpath('//*[@id="post_author_override"]/option[1]')
            yazar.click()
            time.sleep(1)

            # Publish
            browser.execute_script('window.scrollTo(0,0)')
            time.sleep(2)
            browser.find_element_by_xpath('//*[@id="publishing-action"]').click()
            time.sleep(2)
            browser.execute_script('window.scrollTo(0,document.body.scrollHeight)')


            files = os.listdir(customerPath)


            try:
                shutil.rmtree(customerPath+"Contents/"+content[1]) #clear content folder
            except:
                print("silme basarisiz")

            browser.close()
# except:
#     print("big except")
#     browser.close()
#     try:
#         shutil.rmtree(customerPath+"Contents/"+content[1])
#     except:
#         print("silme basarisiz")
except Exception as e: print(e)
