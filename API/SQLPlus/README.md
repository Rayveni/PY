# SQLPlus Api
This python code wraps sql query and passes it to SQL Plus with cmd.
SQL query must not contain skip rows.

[sample](sql_plus_sample.ipynb)

## methods
* set_sql_query(query_params={},sql_path=None,query=None)\
  * query_params - promts in your query
  * sql_path -location of your sql file
  * query -you can pass sql statement directly in text variable(instead sql_path)
  
* prepareload(path)
  * creates directory for load files(existant dir will be removed)
 
* write_query(path='default',query='',display=True) -writes wrapped SQL Query to file (for analisys)
* FetchData(conn_str,savepath,sql=None) -fetches data from sql query
* ThreadPool(f,applylist,n_threads=-1,asyncmap=True) - launches multi threads
 
