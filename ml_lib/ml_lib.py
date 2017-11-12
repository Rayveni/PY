import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  
import seaborn as sns
class stats:

    def __stat_intervals(stat, alpha=0.05):
        boundaries = np.percentile(stat, [100 * alpha / 2, 100 * (1 - alpha / 2)])
        return boundaries    
   
    def __get_bootstrap_samples(array, n_samples,seed=None):
        if type(array)!=np.ndarray:
            array=np.array(array)
        if seed:np.random.seed(seed)
           
        indices = np.random.randint(0, len(array), (n_samples, len(array)))
        samples = array[indices]
        return samples
    
    def __print_conf_int(alpha,text,boundaries):
        print("{:.0%} confidence interval {}:[{:.2f},{:.2f}]".format(1-alpha,text,boundaries[0],boundaries[1]))
        
    @classmethod
    def bootstrap_confint(self,array,n_samples,function=np.mean,alpha=0.05,seed=None,print_text=True,text=''):
        """Function for calculation confidence interval using bootstrap.
        Args:
            array: input data (numpy array or list)
            function: function, applied to each bootsrapped sample
            n_samples: numbder of generated bootstrap samples
            aplpha:confidence level
            seed: random seed
            print_text: enable/disable printing message  with conf interval
            text:extra text added to message
    
        """
        scores =list(map(function, self.__get_bootstrap_samples(array, n_samples,seed)))
        boundaries=self.__stat_intervals(scores, alpha)
        
        if print_text:self.__print_conf_int(alpha,text,boundaries)  
        return boundaries
    
    @classmethod
    def bootstrap_delta_confint(self,array1,array2,n_samples,function=np.mean,alpha=0.05,seed=None,print_text=True,text=''):
        """Function for calculation confidence interval for difference on two samples(array1-array2) using bootstrap.
        Args:
            array1: input data (numpy array or list)
            function: function, applied to each bootsrapped sample
            n_samples: numbder of generated bootstrap samples
            aplpha:confidence level
            seed: random seed
            print_text: enable/disable printing message  with conf interval
            text:extra text added to message
    
        """
        scores1 =map(function, self.__get_bootstrap_samples(array1, n_samples,seed))
        scores2 =map(function, self.__get_bootstrap_samples(array2, n_samples,seed))
        delta_median_scores = list(map(lambda x: x[1] - x[0], zip(scores1, scores2)))
        boundaries=self.__stat_intervals(delta_median_scores, alpha)
        
        if print_text:self.__print_conf_int(alpha,text,boundaries)
        return boundaries

class visualisation:
	pass
class ml:
    @classmethod
    def fast_describe_data(self,data,y,head_rows_num=3):
        from IPython.display import display
        print('Data shape: {} rows,{} columns'.format(data.shape[0],data.shape[1]))
        display(data.head(head_rows_num))
        self.missing_values_count(data)
        display(self.count_data_types(data))
        pass
    	
    def missing_values_count(data,x_title='',y_title='',
                             fig_size=(14,0.5),color="salmon", saturation=.5,
                             show_percent=True,min_perc_show=1,
                             add_height_val=0.7,default_intercept=1):
        
        missing_df = data.isnull().sum(axis=0).reset_index()
        missing_df.columns = ['column_name', 'missing_count']
        missing_df = missing_df[missing_df['missing_count']>0].sort_values(by='missing_count',ascending=False)
        plt.figure(figsize=(fig_size[0],missing_df.shape[0]*fig_size[1]))
        plt.title(y_title)

        bar=sns.barplot(x="missing_count", y="column_name", data=missing_df,color=color, saturation=saturation)

        bar.set(xlabel=x_title, ylabel='')
        if show_percent:
            add_height=add_height_val*bar.patches[0].get_height()
            data_xshape=data.shape[0]
            intercept=default_intercept*bar.patches[0].get_width() /100
            for rect in bar.patches:
                width=rect.get_width()
                perc=np.round(100*width/data_xshape,2)
                if perc>=min_perc_show:
                    plt.text(width+intercept, add_height+rect.get_y(),'{}%'.format(perc))
        plt.title('Missing values')
        plt.show()
        return missing_df
    @staticmethod
    def count_data_types(data):
        dtype_df = data.dtypes.reset_index()
        dtype_df.columns = ["Count", "Column Type"]
        return dtype_df.groupby("Column Type").aggregate('count').reset_index()


class neuralnets:
	pass