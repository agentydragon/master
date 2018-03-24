from src.prototype.lib import article_repo

assert article_repo.sanitize_articletitle('Appolo 2/3') == 'Appolo_2_3'
assert article_repo.sanitize_articletitle('Alger of Liège') == 'Alger_of_Liège'
