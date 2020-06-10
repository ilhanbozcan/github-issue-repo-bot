import requests
import webbrowser
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver

LOGIN = 'https://github.com/session'


headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Accept': '/',
        'Origin': 'https://www.jumbotourscontracts.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }


payload = {
'commit': 'Sign in',
'login': 'username',
'password': 'password.'
}

#driver = webdriver.Firefox()
#driver.get('https://github.com/login')

#LOGIN = driver.page_source



session = requests.Session()
with session as s:
    #s.post(SIGN_IN_URL,data=payload)
    response = s.get(LOGIN)
    soup = BeautifulSoup(response.content, 'html.parser')
    token_val = soup.find(attrs = {"name": "authenticity_token"})['value']
    commit = soup.find(attrs={"name": "commit"})['value']
    timestamp = soup.find(attrs={"name": "timestamp"})['value']
    timestamp_secret = soup.find(attrs={"name": "timestamp_secret"})['value']
    webauthn_iuvpaa_support = 'supported'
    webauthn_support = 'supported'
    #ga_id = soup.find(attrs={"name": "ga_id"})['value']
    print(token_val)
    #print(commit)
    #print(timestamp)
    #print(timestamp_secret)
    #print(webauthn_iuvpaa_support)

    payload['authenticity_token'] = token_val
    payload['webauthn-iuvpaa-support'] = 'supported'
    payload['ga_id'] = ""
    payload['return_to'] = ""
    payload['required_field_28cf'] = ""
    payload['webauthn-support'] = 'supported'
    payload['timestamp'] = timestamp
    payload['timestamp_secret'] = timestamp_secret
    payload['commit'] = commit






    intent = s.post(LOGIN, data=payload)
    if(intent.status_code== 200):
        print('LOGGED IN SUCCESSFULLY')
        repo_name = input('Enter a repository name')
        repo_page = s.get('https://github.com/' + payload.get('login') + '/'+repo_name+'/issues/new')


        #print(repo_page.url)
        if (repo_page.status_code != 200): #repo check
            pick = input('REPO IS NOT EXIST..IF YOU WANT TO CREATE TYPE "yes" AND GO')
            if pick == 'yes':
                new_repo_content = s.get('https://github.com/new')
                #print(new_repo_content.url)
                new_repo_data = {
                    'owner': payload.get('login'),
                    'repository[name]': repo_name,
                    'repository[description]': 'Bot repo',
                    'repository[visibility]': 'public',
                    'repository[auto_init]': 0,
                }
                soup = BeautifulSoup(new_repo_content.content, 'html.parser')
                form = (soup.find(attrs={"id": "new_repository"}))
                input = form.find_all('input')

                #print(input[0]['value'])  # token
                new_repo_data['authenticity_token'] = input[0]['value']

                intent = s.post('https://github.com/repositories', data=new_repo_data)
                if(intent.status_code==200):
                    print('REPO CREATED')
                else:
                    print('REPO IS NOT CREATED')



        ###ISSUE CREATION PART


        title = input('Enter a issue title')
        body = input('Enter a issue content')
        issue_info = {
            'issue[body]': body,
            'issue[title]': title,
        }

        repo_page = s.get('https://github.com/' + payload.get('login') + '/' + repo_name + '/issues/new')

        soup = BeautifulSoup(repo_page.content, 'html.parser')

        ##get datas

        form = (soup.find(attrs={"id": "new_issue"}))
        input = form.find_all('input')

        #print(input[0]['value'])  # token
        #print(input[1]['name'])  # PArsing for requried field because required filed parameter name change automaticlly
        #print(input[2]['value'])  # timestamp
        #print(input[3]['value'])  # timestamp_secret

        ##set datas
        issue_info['authenticity_token'] = input[0]['value']
        issue_info['timestamp'] = input[2]['value']
        issue_info['timestamp_secret'] = input[3]['value']
        issue_info['base_commit_oid'] = ""
        issue_info['comment_id'] = ""
        issue_info['end_commit_oid'] = ""
        issue_info['issue[body_template_name]'] = ""
        issue_info['issue[user_assignee_ids][]'] = ""
        issue_info['line'] = ""
        issue_info['path'] = ""
        issue_info['preview_side'] = ""
        issue_info['preview_start_side'] = ""
        issue_info[str(input[1]['name'])] = ""
        issue_info['saved_reply_id'] = ""
        issue_info['start_commit_oid'] = ""
        issue_info['start_line'] = ""

        intent = s.post('https://github.com/' + payload.get('login') + '/'+repo_name+'/issues/', data=issue_info)
        if intent.status_code == 200:
            print('ISSUES CREATEDDD')

        else:
            print('DATA IS NOT EQUAL WITH POST REQUIREMENT')



    else:
        print('SOMETHING WRONG')




