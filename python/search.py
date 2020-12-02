from flask import Flask
from flask import render_template
from flask import request
import requests
from github import Github

app = Flask(__name__)

ACCESS_TOKEN = 'dfd19231c182386ad4163924a764d244b71b25e6'

g = Github(ACCESS_TOKEN)

@app.route('/')
def search_test():
   return render_template('search.html')


@app.route('/resultset',methods = ['POST', 'GET'])
def resultset():
    if request.method == 'POST':

        print(request.form.keys)
        keyword = request.form['query']
        print(keyword)


        rate_limit = g.get_rate_limit()
        
        rate = rate_limit.search
        
        if rate.remaining == 0:
            print('You have 0/{rate.limit} API calls remaining. Reset time: {rate.reset}')
            return
        else:
            print('You have {rate.remaining}/{rate.limit} API calls remaining')

        query = keyword+' in:file extension:sql language:PLpgSQL repo:letsbikash/database'
        print(query)

        github_url = g.search_code(query, order='desc')

        max_size = 5
        print('Found {github_url.totalCount} file(s)')

        if github_url.totalCount > max_size:
            github_url = github_url[:max_size]
            
        
        try:
            result=github_url[0].download_url

            r = requests.get(result)

            a=r.content.decode("utf-8").split('\n')
            st=None
            end=None

            for i in range(len(a)):
                print(i,a[i],st)
                if (st is None) and ';' in a[i]:
                    first=i
                if st is None and keyword.upper() in a[i].upper():
                    st=i
                if st and ';' in a[i]:
                    end=i
                    break

            return '<body style="color:blue""><h2><pre>'+'<br>'.join(a[first+1:end+1])+'</pre></h2></body'
        except:
            return '<body><h2><pre> I am learning . Sorry.. 😔  Will find something next time </pre></h2></body'


if __name__ == '__main__':
   app.run(debug = True)
   


