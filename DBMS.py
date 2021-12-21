### TODO
### Διμιουργησε πειραματα για την Quad_Tree.remove και εκτελεσε τα

import os
def delete_line(file_index,d_element):
    file_index.flush()
    file_index.seek(0,0)
    buffer=file_index.readlines()
    file_index.close()
    file_index=open(file_index.name,'w+')
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
            sum_records+=child.size
        if sum_records==0:
            file_name=self.children[0].file_name[:len(self.children[0].file_name)-5]
            new_Leaf=Leaf(self.x,self.y,self.width,self.height,file_name+'.csv',self.parent,self.parent_index)
            for child in self.children:
                child.file.close()
                os.remove(child.file.name)
            self.parent.children[self.parent_index]=new_Leaf

class Leaf(Node):
    def __init__(self, x, y, width, height,file_name,parent,parent_index):
        super().__init__(x, y, width, height)
        self.file_name=file_name
        self.file=open('./Data_Blocks/'+file_name,'w+')
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
                    ###new_Noode.children[2].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[2].file.write(data_line)###REMOVE
                    new_Node.children[2].file.flush()###REMOVE
                    new_Node.children[2].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[2].file_name)
                else:
                     ###new_Noode.children[0].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[0].file.write(data_line)###REMOVE
                    new_Node.children[0].file.flush()###REMOVE
                    new_Node.children[0].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[0].file_name)
            else:
                if y_data_line>=self.y and y_data_line<=self.y+self.height/2:
                     ###new_Noode.children[2].insert(data_line.split(',')[3]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[3].file.write(data_line)###REMOVE
                    new_Node.children[3].file.flush()###REMOVE
                    new_Node.children[3].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[3].file_name)
                else:
                     ###new_Noode.children[1].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[1].file.write(data_line)###REMOVE
                    new_Node.children[1].file.flush()###REMOVE
                    new_Node.children[1].size+=1
                    combs_id_filename.append(data_line.split(',')[0]+','+new_Node.children[1].file_name)
        #CHECK THE NEW RECORD
        if x>=self.x and x<=self.x+self.width/2:
                if y>=self.y and y<=self.y+self.height/2:
                     ###new_Noode.children[2].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[2].file.write(id+','+str(x)+','+str(y)+','+time+'\n')###REMOVE
                    new_Node.children[2].file.flush()###REMOVE
                    new_Node.children[2].size+=1
                    combs_id_filename.append(id+','+new_Node.children[2].file_name)
                else:
                     ###new_Noode.children[0].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[0].file.write(id+','+str(x)+','+str(y)+','+time+'\n')###REMOVE
                    new_Node.children[0].file.flush()###REMOVE
                    new_Node.children[0].size+=1
                    combs_id_filename.append(id+','+new_Node.children[0].file_name)
        else:
                if y>=self.y and y<=self.y+self.height/2:
                     ###new_Noode.children[3].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[3].file.write(id+','+str(x)+','+str(y)+','+time+'\n')###REMOVE
                    new_Node.children[3].file.flush()###REMOVE
                    new_Node.children[3].size+=1
                    combs_id_filename.append(id+','+new_Node.children[3].file_name)
                else:
                     ###new_Noode.children[1].insert(data_line.split(',')[0]+','+str(x_data_line)+','+str(y_data_line)+','data_line.split(',')[3]+'\n')###ADD
                    new_Node.children[1].file.write(id+','+str(x)+','+str(y)+','+time+'\n')###REMOVE
                    new_Node.children[1].file.flush()###REMOVE
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

class Quad_Tree:
    def __init__(self,x,y,width,height,max_leaf_size):
        Quad_Tree.root=Leaf(x,y,width,height,'0.csv',None,-1)
        Quad_Tree.max_leaf_size=max_leaf_size
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
    def rangeQuery(r):
        return None

class Hash_Index:
    def __init__(self):
        Hash_Index.hash_map=open('./hash_map.csv','w+')
    def remove(id):
        Hash_Index.hash_map.seek(0,0)
        for index_line in Hash_Index.hash_map.readlines():
            if index_line.split(',')[0]==id:
                block=open('./Data_Blocks/'+index_line.split(',')[1].strip())
                for block_line in block.readlines():
                    if block_line.split(',')[0]==id:
                        x=float(block_line.split(',')[1])
                        y=float(block_line.split(',')[2])
                        Hash_Index.hash_map=delete_line(Hash_Index.hash_map,id)
                        block.close()
                        return (x,y)
        return (None,None)


####REMOVE###
################################## TESTING ###########################################################

    # #CLEAN DATA BLOCKS
    # for file in os.listdir('./Data_Blocks'):
    #     os.remove('./Data_Blocks/'+file)

#     #TEST TREE
# Hash_Index()
# Quad_Tree(0,0,10,10,4)
# # Quad_Tree.max_leaf_size=4
# # Quad_Tree.root=Inner_Node(0,0,10,10,None,-1)

# # leaf_00=Leaf(0,5,5,5,'00.csv',Quad_Tree.root,0)
# # inner_node_01=Inner_Node(5,5,5,5,Quad_Tree.root,1)
# # leaf_02=Leaf(0,0,5,5,'02.csv',Quad_Tree.root,2)
# # inner_node_03=Inner_Node(5,0,5,5,Quad_Tree.root,3)
# # leaf_010=Leaf(5,7.5,2.5,2.5,'010.csv',inner_node_01,0)
# # leaf_011=Leaf(7.5,7.5,2.5,2.5,'011.csv',inner_node_01,1)
# # leaf_012=Leaf(5,5,2.5,2.5,'012.csv',inner_node_01,2)
# # leaf_013=Leaf(7.5,5,2.5,2.5,'013.csv',inner_node_01,3)
# # leaf_030=Leaf(5,2.5,2.5,2.5,'030.csv',inner_node_03,0)
# # leaf_031=Leaf(7.5,2.5,2.5,2.5,'031.csv',inner_node_03,1)
# # leaf_032=Leaf(5,0,2.5,2.5,'032.csv',inner_node_03,2)
# # leaf_033=Leaf(7.5,0,2.5,2.5,'033.csv',inner_node_03,3)

# # inner_node_01.children.append(leaf_010)
# # inner_node_01.children.append(leaf_011)
# # inner_node_01.children.append(leaf_012)
# # inner_node_01.children.append(leaf_013)

# # inner_node_03.children.append(leaf_030)
# # inner_node_03.children.append(leaf_031)
# # inner_node_03.children.append(leaf_032)
# # inner_node_03.children.append(leaf_033)


# # Quad_Tree.root.children.append(leaf_00)
# # Quad_Tree.root.children.append(inner_node_01)
# # Quad_Tree.root.children.append(leaf_02)
# # Quad_Tree.root.children.append(inner_node_03)

# # leaf_030.insert('id1',5.5,4,'22:30')
# # leaf_030.insert('id2',6,4.5,'22:30')
# # leaf_030.insert('id3',6.5,4,'22:30')
# # leaf_030.insert('id4',7,4.5,'22:30')
# # leaf_030.insert('id5',6,2.55,'22:30')

# #00-leaf
# Quad_Tree.insert('id1',1,7,'22:00')
# Quad_Tree.insert('id2',2,8,'22:00')
# Quad_Tree.insert('id3',3,9,'22:00')
# Quad_Tree.insert('id4',4,10,'22:00')

# #02-leaf
# Quad_Tree.insert('id21',0,0,'22:00')
# Quad_Tree.insert('id22',1,1,'22:00')
# Quad_Tree.insert('id23',2,2,'22:00')
# Quad_Tree.insert('id24',3,3,'22:00')

# #030-leaf
# Quad_Tree.insert('id25',5.1,2.51,'22:00')
# Quad_Tree.insert('id26',5.5,3,'22:00')
# Quad_Tree.insert('id27',6,3.5,'22:00')
# Quad_Tree.insert('id28',7,4,'22:00')

# #031-leaf
# Quad_Tree.insert('id29',7.51,2.51,'22:00')
# Quad_Tree.insert('id30',8,3,'22:00')
# Quad_Tree.insert('id31',8.5,3.5,'22:00')
# Quad_Tree.insert('id32',9,4,'22:00')

# #032-leaf
# Quad_Tree.insert('id33',5.1,0.1,'22:00')
# Quad_Tree.insert('id34',5.5,0.5,'22:00')
# Quad_Tree.insert('id35',6,1,'22:00')
# Quad_Tree.insert('id36',6.5,1.5,'22:00')

# #033-leaf
# Quad_Tree.insert('id37',7.51,0.1,'22:00')
# Quad_Tree.insert('id38',8,0.5,'22:00')
# Quad_Tree.insert('id39',8.5,1,'22:00')
# Quad_Tree.insert('id40',9,1.5,'22:00')

# #---------------------------------------------------------------------------------------
# #MOVE leafs 03* to 01
# #010-leaf
# Quad_Tree.insert('id25',5.1,7.51,'23:30')
# Quad_Tree.insert('id26',5.5,8,'23:30')
# Quad_Tree.insert('id27',6,8.5,'23:30')
# Quad_Tree.insert('id28',7,9,'23:30')

# #011-leaf
# Quad_Tree.insert('id29',7.51,7.51,'23:30')
# Quad_Tree.insert('id30',8,8,'23:30')
# Quad_Tree.insert('id31',8.5,8.5,'23:30')
# Quad_Tree.insert('id32',9,9,'23:30')

# #012-leaf
# Quad_Tree.insert('id33',5.1,5.1,'23:30')
# Quad_Tree.insert('id34',5.5,5.5,'23:30')
# Quad_Tree.insert('id35',6,6,'23:30')
# Quad_Tree.insert('id36',6.5,6.5,'23:30')

# #013-leaf
# Quad_Tree.insert('id37',7.51,5.1,'23:30')
# Quad_Tree.insert('id38',8,5.5,'23:30')
# Quad_Tree.insert('id39',8.5,6,'23:30')
# Quad_Tree.insert('id40',8.5,6.5,'23:30')