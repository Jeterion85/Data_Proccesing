import os
import geopy.distance

def delete_line(file_index,d_element):
    file_index.flush()
    file_index.seek(0,0)
    buffer=file_index.readlines()
    file_index.close()
    file_index=open(file_index.name,'w+',encoding='ASCII')
    for block_line in buffer:
        if block_line.split(',')[0]!=d_element:
            file_index.write(block_line)
            file_index.flush()
    return file_index

class Node:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
    
class Inner_Node(Node):
    def __init__(self, x, y, width, height,parent,parent_index):
        super().__init__(x, y, width, height)
        self.children=[]
        self.parent=parent
        self.parent_index=parent_index
    def compact(self):
        sum_records=0
        for child in self.children:
            if child.__class__.__name__!='Leaf':
                sum_records+=1
                continue
            sum_records+=child.size
        if sum_records==0:
            file_name=self.children[0].file_name[:len(self.children[0].file_name)-5]
            new_Leaf=Leaf(self.x,self.y,self.width,self.height,file_name+'.csv',self.parent,self.parent_index)
            for child in self.children:
                child.file.close()
                os.remove(child.file.name)
            self.parent.children[self.parent_index]=new_Leaf
            self.parent.compact()

class Leaf(Node):
    def __init__(self, x, y, width, height,file_name,parent,parent_index):
        super().__init__(x, y, width, height)
        self.file_name=file_name
        self.file=open('./Data_Blocks/'+file_name,'w+',encoding='ASCII')
        self.size=0
        self.parent=parent
        self.parent_index=parent_index
    def insert(self,id,x,y,time):
        if self.size+1>Quad_Tree.max_leaf_size:
            self.split_leaf(id,x,y,time)
        else:
            self.file.write(id+','+str(x)+','+str(y)+','+time+'\n')
            self.file.flush()
            self.size+=1
            Hash_Index.hash_map.write(id+','+self.file_name+'\n')
            Hash_Index.hash_map.flush()
    def split_leaf(self,id,x,y,time):
        new_Node=Inner_Node(self.x,self.y,self.width,self.height,self.parent,self.parent_index)
        new_Node.children.append(Leaf(self.x,self.y+self.height/2,self.width/2,self.height/2,self.file_name.split('.')[0]+'0.csv',new_Node,0))
        new_Node.children.append(Leaf(self.x+self.width/2,self.y+self.height/2,self.width/2,self.height/2,self.file_name.split('.')[0]+'1.csv',new_Node,1))
        new_Node.children.append(Leaf(self.x,self.y,self.width/2,self.height/2,self.file_name.split('.')[0]+'2.csv',new_Node,2))
        new_Node.children.append(Leaf(self.x+self.width/2,self.y,self.width/2,self.height/2,self.file_name.split('.')[0]+'3.csv',new_Node,3))
        combs_id_filename=[]
        #CHECK FOR DATA IN BLOCK
        self.file.seek(0,0)
        for data_line in self.file.readlines():
            x_data_line=float(data_line.split(',')[1])
            y_data_line=float(data_line.split(',')[2])
            if x_data_line>=self.x and x_data_line<=self.x+self.width/2:
                if y_data_line>=self.y and y_data_line<=self.y+self.height/2:
                    new_Node.children[2].file.write(data_line)
                    new_Node.children[2].file.flush()
                    new_Node.children[2].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[2].file_name)
                else:
                    new_Node.children[0].file.write(data_line)
                    new_Node.children[0].file.flush()
                    new_Node.children[0].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[0].file_name)
            else:
                if y_data_line>=self.y and y_data_line<=self.y+self.height/2:
                    new_Node.children[3].file.write(data_line)
                    new_Node.children[3].file.flush()
                    new_Node.children[3].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[3].file_name)
                else:
                    new_Node.children[1].file.write(data_line)
                    new_Node.children[1].file.flush()
                    new_Node.children[1].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[1].file_name)
        #PLACE THE NEW RECORD
        if id!=None:
            if x>=self.x and x<=self.x+self.width/2:
                    if y>=self.y and y<=self.y+self.height/2:
                        new_Node.children[2].file.write(id+','+str(x)+','+str(y)+','+time+'\n')
                        new_Node.children[2].file.flush()
                        new_Node.children[2].size+=1
                        combs_id_filename.append(id+','+new_Node.children[2].file_name)
                    else:
                        new_Node.children[0].file.write(id+','+str(x)+','+str(y)+','+time+'\n')
                        new_Node.children[0].file.flush()
                        new_Node.children[0].size+=1
                        combs_id_filename.append(id+','+new_Node.children[0].file_name)
            else:
                    if y>=self.y and y<=self.y+self.height/2:
                        new_Node.children[3].file.write(id+','+str(x)+','+str(y)+','+time+'\n')
                        new_Node.children[3].file.flush()
                        new_Node.children[3].size+=1
                        combs_id_filename.append(id+','+new_Node.children[3].file_name)
                    else:
                        new_Node.children[1].file.write(id+','+str(x)+','+str(y)+','+time+'\n')
                        new_Node.children[1].file.flush()
                        new_Node.children[1].size+=1
                        combs_id_filename.append(id+','+new_Node.children[1].file_name)
        self.file.close()
        os.remove(self.file.name)
        if self.parent==None:#If root
            Quad_Tree.root=new_Node
        else:
            self.parent.children[self.parent_index]=new_Node
        
        for comb in combs_id_filename:
            Hash_Index.hash_map=delete_line(Hash_Index.hash_map,comb.split(',')[0])
            Hash_Index.hash_map.write(comb+'\n')    
            Hash_Index.hash_map.flush()
        #CHECK FOR SECOND OVERFLOW AND SPLIT AGAIN THE LEAF THAT HAPPENS
        for child in new_Node.children:
            if child.size > Quad_Tree.max_leaf_size:
                child.split_leaf(None,-1,-1,None)

class Quad_Tree:
    def __init__(self,x,y,width,height,max_leaf_size):
        Quad_Tree.root=Leaf(x,y,width,height,'0.csv',None,-1)
        Quad_Tree.max_leaf_size=max_leaf_size
        Quad_Tree.range_query_results=[]
    def insert(id,x,y,time):
        x_previous,y_previous=Hash_Index.remove(id)
        Quad_Tree.remove(id,x_previous,y_previous)
        current_Node=Quad_Tree.root
        while current_Node.__class__.__name__!='Leaf':
            if x>=current_Node.x and x<=current_Node.x+current_Node.width/2:
                if y>=current_Node.y and y<=current_Node.y+current_Node.height/2:
                    current_Node=current_Node.children[2]
                else:
                    current_Node=current_Node.children[0]
            else:
                if y>=current_Node.y and y<=current_Node.y+current_Node.height/2:
                    current_Node=current_Node.children[3]
                else:
                    current_Node=current_Node.children[1]
        current_Node.insert(id,x,y,time)
    def remove(id,x,y):
        if x!=None:
            current_Node=Quad_Tree.root
            while current_Node.__class__.__name__!='Leaf':
                if x>=current_Node.x and x<=current_Node.x+current_Node.width/2:
                    if y>=current_Node.y and y<=current_Node.y+current_Node.height/2:
                        current_Node=current_Node.children[2]
                    else:
                        current_Node=current_Node.children[0]
                else:
                    if y>=current_Node.y and y<=current_Node.y+current_Node.height/2:
                        current_Node=current_Node.children[3]
                    else:
                        current_Node=current_Node.children[1]
            current_Node.file=delete_line(current_Node.file,id)
            current_Node.size-=1
            if current_Node.parent!=None:
                current_Node.parent.compact()
    def rangeQuery(x,y,r,x_r_MBR,y_r_MBR,width_r_MBR,height_r_MBR,node):
        if node.__class__.__name__=='Leaf':
           #REFIMENT
           block=open('./Data_Blocks/'+node.file_name,'r')
           for block_line in block.readlines():
               block_line.strip()
               x_block=float(block_line.split(',')[1])
               y_block=float(block_line.split(',')[2])
               point1=(x_block,y_block)
               point2=(x,y)
               if geopy.distance.distance(point1,point2).km<=r:
                   Quad_Tree.range_query_results.append(block_line)
        else:
            for child in node.children:
                if Quad_Tree.mbrs_interact(x_r_MBR,y_r_MBR,width_r_MBR,height_r_MBR,node):
                    Quad_Tree.rangeQuery(x,y,r,x_r_MBR,y_r_MBR,width_r_MBR,height_r_MBR,child)
    def mbrs_interact(x_r_MBR,y_r_MBR,width_r_MBR,height_r_MBR,node): 
        rect1=Rectangle(x_r_MBR,y_r_MBR,width_r_MBR,height_r_MBR)
        rect2=Rectangle(node.x,node.y,node.width,node.height)
        if (rect1.l.x == rect1.r.x or rect1.l.y == rect1.r.y or rect2.l.x == rect2.r.x or rect2.l.y == rect2.r.y):
            return False
     
        if(rect1.l.x > rect2.r.x or rect2.l.x > rect1.r.x):
            return False

        if(rect1.r.y > rect2.l.y or rect2.r.y > rect1.l.y):
            return False
 
        return True
        
class Hash_Index:
    def __init__(self):
        Hash_Index.hash_map=open('./hash_map.csv','w+',encoding='ASCII')
    def remove(id):
        Hash_Index.hash_map.seek(0,0)
        for index_line in Hash_Index.hash_map.readlines():
            if index_line.split(',')[0]==id:
                block=open('./Data_Blocks/'+index_line.split(',')[1].strip(),encoding='ASCII')
                for block_line in block.readlines():
                    if block_line.split(',')[0]==id:
                        x=float(block_line.split(',')[1])
                        y=float(block_line.split(',')[2])
                        Hash_Index.hash_map=delete_line(Hash_Index.hash_map,id)
                        block.close()
                        return (x,y)
        return (None,None)
class Rectangle:
    def __init__(self,x,y,width,height):
        self.l=Point(x,y+height)
        self.r=Point(x+width,y)

class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
