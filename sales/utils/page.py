

from django.utils.safestring import mark_safe


class MyPagenation():
    def __init__(self,page,customer_count):
        self.customer_count = customer_count
        self.per_page_num = 10

        a, b = divmod(self.customer_count, self.per_page_num)

        if not b:
            page_num_count = a
        else:
            page_num_count = a+ 1

        try:
            page = int(page)
            if page <= 0:
                page = 1
            elif page > page_num_count:

                page = page_num_count
        except Exception:
            page = 1
        self.page = page
        self.page_num_count = page_num_count
        page_num_show = 3
        if page < 4:
            start_page_num = 1
            end_page_num = 8
        elif page > page_num_count - page_num_show:
            start_page_num = page_num_count - (2 * page_num_show)
            end_page_num = page_num_count + 1
        else:
            start_page_num = page - page_num_show
            end_page_num = page + page_num_show + 1
        self.start_page_num =start_page_num
        self.end_page_num =end_page_num
        self.page_num_show = page_num_show
    def page_html(self ):
        self.page_html = ''
        self.page_pre_html = '<nav aria-label="Page navigation"><ul class="pagination"><li><a href="/customers/?page{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.page - 1)
        self.page_num_html = '<li><a href="/customers/?page={{ foo }}" >{{ foo }}</a></li>'
        if self.page <= 1:
            self.page_html += self.page_pre_html
        else:
            self.page_html += '<nav aria-label="Page navigation"><ul class="pagination"><li class="disabled"><a href="/customers/?page{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.page - 1)
        for i in range(self.start_page_num, self.end_page_num):
            if i ==self.page:

                self.page_html += '<li class="active"><a href="/customers/?page={0}" >{0}</a></li>'.format(i)
            else:
                self.page_html+='<li><a href="/customers/?page={0}" >{0}</a></li>'.format(i)
        self.page_next_html = ' <li><a href="#" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li></ul></nav>'
        if self.page < self.page_num_count:
            self.page_html += self.page_next_html
        else:
            self.page_html +=  '<li class="active"><a href="/customers/?page={0}}" aria-label="Next">{0}<span aria-hidden="true">&raquo;</span></a></li></ul></nav>'.format('kw=2222&search_field=qq&page=%s'%self.page+1)

        return mark_safe(self.page_html)