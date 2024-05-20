# 安裝 geckodriver，這是 Firefox WebDriver 的驅動程式。
from selenium import webdriver
from selenium.webdriver.common.by import By
# 前往特定頁面，點擊 follow 按鈕
from selenium import webdriver
# 用於生成複雜的使用者交互，比如滑鼠移動、點擊、拖放等
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pickle
from bs4 import BeautifulSoup
import pandas as pd


# 初始化 Firefox WebDriver
options = webdriver.FirefoxOptions()
# options.add_argument('--headless')  # 選擇無頭模式，不顯示瀏覽器窗口

driver = webdriver.Firefox(options=options)

# 1. 登入 IG
# 嘗試加載保存的 cookie
try:
    # 加載保存的 cookie
    driver.get('https://www.instagram.com/accounts/login/')
    cookies = pickle.load(open("instagram_cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    # 刷新頁面或前往目標頁面
    driver.refresh()  # 刷新頁面

    time.sleep(random.uniform(3, 5))

    # 確認是否成功保持登入狀態
    current_url = driver.current_url
    print("當前頁面 URL:", current_url)

except (FileNotFoundError, pickle.UnpicklingError):
    # 如果找不到保存的 cookie 文件，或者加載 cookie 出錯，則需要重新登入
    print("找不到保存的 cookie 文件，或者加載 cookie 出錯，需要重新登入。")

    # 前往 Instagram 登入頁面
    driver.get('https://www.instagram.com/accounts/login/')

    time.sleep(5)

    # 找到帳號和密碼的輸入框，並輸入登入資訊
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    # 輸入帳號和密碼
    username = 'your_username'
    password = 'your_password'

    username_input.send_keys(username)
    password_input.send_keys(password)

    # 找到登入按鈕，並模擬點擊
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # 等待登入完成
    time.sleep(10) 

    # 獲取當前頁面的 URL，用於確認是否成功登入
    current_url = driver.current_url
    if 'instagram.com/accounts/login/' not in current_url:
        # 登入成功，獲取並保存 cookie
        pickle.dump(driver.get_cookies(), open("instagram_cookies.pkl", "wb"))
        print("成功登入並保存 cookie。")

    else:
        print("登入失敗或需要進一步操作，無法保存 cookie。")


# 2. 登入成功，前往目標頁面

if 'instagram.com/accounts/login/' not in driver.current_url:
    target_url = 'https://www.instagram.com/group_buy_note/'  # 替換成目標頁面
    driver.get(target_url)
else:
    print("登入失敗或需要進一步操作，無法前往目標頁面。")

# 等待目標頁面加載完成
time.sleep(random.uniform(3, 5))

# 獲取當前頁面的 URL，用於確認是否成功進入目標頁面
current_url = driver.current_url
print("當前頁面 URL:", current_url)


# 3. 等待 "Following" 按鈕出現並點擊
try:
    # 使用 XPath 表達式來尋找 href 包含 /following/ 的 <a> 標籤
    following_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/following/")]'))
    )
    print("找到了 Following 按鈕")

    # 使用 ActionChains 點擊按鈕
    actions = ActionChains(driver)
    actions.move_to_element(following_button).click().perform()
    print("點擊了 Following 按鈕")

    # 可選：等待 Following 頁面加載完成
    time.sleep(random.uniform(3, 5))
except Exception as e:
    print("找不到 Following 按鈕或點擊失敗:", str(e))


# 4. 模擬滾動到 following 列表最底部

# 定位特定區域的元素（使用提供的 class 名稱）
class_name = '_aano'
target_element = driver.find_element(By.CLASS_NAME, class_name)

# 初始滾動高度和前一次滾動高度
last_height = 0
scroll_height = 0

while True:
    # 滾動到目前的滾動位置 + 1000 的高度，設置平滑滾動效果
    driver.execute_script('arguments[0].scrollTo({ top: arguments[1], behavior: "smooth" });', target_element, scroll_height + 1000)
    
    # 等待一段時間，讓頁面加載完成
    time.sleep(random.uniform(2, 6))
    
    # 獲取目前的滾動高度
    scroll_height = driver.execute_script('return arguments[0].scrollTop;', target_element)
    print("目前的滾動高度:", scroll_height)
    
    # 獲取頁面的高度
    current_height = driver.execute_script('return arguments[0].scrollHeight;', target_element)
    # print("頁面的高度:", current_height)

    # 判斷是否已經到達頁面底部或無法再滾動
    if scroll_height == last_height:
        print("已無法再滾動，滾動結束。")
        break
    
    # 更新上一次滾動的高度
    last_height = scroll_height
    # print("上一次滾動的高度:", last_height)
    print("-------------------")


# 5. 獲取 Instagram 追蹤者列表

# 獲取頁面源碼
page_source = driver.page_source
# print(page_source)

# 使用 BeautifulSoup 解析頁面源碼
soup = BeautifulSoup(page_source, 'html.parser')
# print(soup)

# 假設 followers_list 已經被正確地提取出來
followers_list = soup.find_all('div', class_='x1dm5mii')

# 創建列表來存儲數據
data = []

for follower in followers_list:
    # 找到追蹤者的帳號名稱
    username_tag = follower.find('a', class_='x1i10hfl')
    if username_tag:
        username = username_tag['href'].strip('/')
    
    # 找到追蹤者的全名
    full_name_tag = follower.find('span', class_='x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft') 
    if full_name_tag:
        full_name = full_name_tag.text
    
    # 打印帳號名稱和全名
    print(f"Username: {username}")
    print(f"Full Name: {full_name}")

    # 建立追蹤者帳號連結
    profile_link = f'https://www.instagram.com/{username}/'
    print(f"Profile Link: {profile_link}")
    print("----------------------------")
    # 添加到數據列表
    data.append([username, full_name, profile_link])


# 6. 匯出成 CSV 文件

# 創建 DataFrame
df = pd.DataFrame(data, columns=["Username", "Full Name", "Profile Link"])
print(df)

# 匯出成 CSV 文件
df.to_csv('instagram_followers.csv', index = False)

print("資料已成功匯出至：instagram_followers.csv.")