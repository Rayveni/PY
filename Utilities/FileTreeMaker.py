
# coding: utf-8
def FileTreeMaker(TreeRoot,skip=[]):  
    import os
    separator=os.path.join(' ',' ')[1:-1]
    
    depthfunc=lambda path:max(len(path.split('/')),len(path.split(separator)))
    rootDepth=depthfunc(TreeRoot)
    
    skip=list(map(lambda t:os.path.normpath(t).split(separator), skip))
    skip=[[el,len(el)+rootDepth]for el in skip]
  
    filesdict={}
    lvlfolderscountdict={}
    
    prevlevel=-1
    filepreindent=r"┃ "
    bodypostfix="┣━"
    endpostfix="┗━"
    emptyprefix='  '
    
    def skipfolders(path):
        res=False
        for skipfolder in skip:
            if path.split(separator)[rootDepth:skipfolder[1]]==skipfolder[0]:
                res=True
                break
        return res
                    
    def PrintFiles(arr):
        for i in range(prevlevel,level-1,-1):  
            cut=i-prevlevel-1
            
            if len(filesdict[i])>0:
                prefix=''
                postfix=''
                if i>0: 
                    prefix=''.join(PrefixArr[:cut])
                    postfix=filepreindent 

                if i>0 and lvlfolderscountdict[i-1][0] <1 and lvlfolderscountdict[i-1][1] ==0 :postfix=emptyprefix
                if lvlfolderscountdict[i][2]==0:postfix+=emptyprefix
                
                prefix=prefix+postfix
            
                for  file in filesdict[i][:-1]:
                    print(prefix+bodypostfix+file)
                print(prefix+endpostfix+filesdict[i][-1])     

    def FolderIntend():
        res=[]  
        for i in range(level): 
            if i==level-1:          
                if lvlfolderscountdict[i][1] >0 or lvlfolderscountdict[i][0]>1 :
                    step=bodypostfix
                elif lvlfolderscountdict[i][0] <=1 :step=endpostfix               
            else: 
                if lvlfolderscountdict[i][0] <1 and lvlfolderscountdict[i][1] ==0 :step=emptyprefix
                else:step=filepreindent
            res.append(step)
            if i==level-1:lvlfolderscountdict[i][0]-=1   
        return res
    
    for root, dirs, files in os.walk(TreeRoot):
        skipprint=skipfolders(root)
 
        if skipprint:
            files=[]
            dirs=[]

        level=depthfunc(root)-depthfunc(TreeRoot)
        
        if level<=prevlevel:   
            PrintFiles(filesdict)
        else:postfix=endpostfix
        
        filesdict[level]=files
        lvlfolderscountdict[level]=[len(dirs),len(files),len(dirs)] 
        PrefixArr=FolderIntend()
        
        if not skipprint:
            if level>0 :print(''.join(PrefixArr)+'['+os.path.basename(root)+']')
            else:print(os.path.basename(root))

        prevlevel=level
    level=0
    PrintFiles(filesdict)


