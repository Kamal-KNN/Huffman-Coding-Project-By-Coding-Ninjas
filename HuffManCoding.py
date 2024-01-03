import os
import heapq
class BinaryTreeNode:
    def __init__(self,value,freq):
        self.value=value
        self.freq=freq
        self.left=None
        self.right=None
    def __lt__(self,other):
        return self.freq<other.freq
    def __eq__(self,other):
        return self.freq==other.freq
class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=list()
        self.__codes=dict()
        self.__recursive_bits=dict()

    def __Build_dict(self,text):
        freq_dict=dict()
        for key in text:
            if key not in freq_dict:
                freq_dict[key]=0
            freq_dict[key]+=1
        return freq_dict
    def __Build_min_heap(self,dictionary):
        for key in dictionary:
            freq=dictionary[key]
            node=BinaryTreeNode(key,freq)
            heapq.heappush(self.__heap,node)
        return
    def __Build_Binary_tree(self):
        while len(self.__heap)>1:
            node1=heapq.heappop(self.__heap)
            node2=heapq.heappop(self.__heap)
            merged_code=BinaryTreeNode(None,node1.freq+node2.freq)
            merged_code.left=node1
            merged_code.right=node2
            heapq.heappush(self.__heap,merged_code)
        return
    def __Build_codes_helper(self,root,codebits):
        if root is None:
            return
        # induction step
        if root.value is not None:
            self.__codes[root.value]=codebits
            self.__recursive_bits[codebits]=root.value
            return
        self.__Build_codes_helper(root.left,codebits+"0")
        self.__Build_codes_helper(root.right,codebits+"1")

    def __Build_codes(self):
        root=heapq.heappop(self.__heap)
        self.__Build_codes_helper(root,"")
    def __Build_encoding_task(self,text):
        encoded_text=""
        for i in text:
            encoded_text=encoded_text+self.__codes[i]
        return encoded_text
    def __padding(self,text):
        paded_amount=8-(len(text)%8)
        for i in range(paded_amount):
            text=text+"0"
        pading_info="{0:08b}".format(paded_amount)
        paded_text=pading_info+text
        return paded_text
    def __binary_array(self,paded_array):
        array=list()
        for i in range(0,len(paded_array),8):
            bytes=paded_array[i:i+8]
            array.append(int(bytes,2))
        return array


    def compress(self):
        # make dict-table
        # make min heap from that
        # make binary tree from that
        # Build codes from Binary Tree
        # Make Encoded_text from Binary tree
        # Add padding it to the text
        # conversion of binary file
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+".bin"
        with open(self.path,'r+') as file ,open(output_path,"wb") as output:
            text=file.read()
            text=text.rstrip()


            freq_dict=self.__Build_dict(text)
            self.__Build_min_heap(freq_dict)
            self.__Build_Binary_tree()
            self.__Build_codes()
            encoded_text=self.__Build_encoding_task(text)
            padded_text=self.__padding(encoded_text)
            padded_binary_array=self.__binary_array(padded_text)
            final_array=bytes(padded_binary_array)
            print("Compressed")
            output.write(final_array)

        return output_path
    def __remove_padding(self,text):
        padding_info=text[:8]
        padding_amount=int(padding_info,2)
        text=text[8:]
        actual_text=text[:-1*padding_amount]
        return actual_text
    def __decoding_text(self,text):
        encoding_text=""
        string_code=""
        for bit in text:
            string_code+=bit
            if string_code in self.__recursive_bits:
                character=self.__recursive_bits[string_code]
                encoding_text+=character
                string_code=""
        return encoding_text

    def decompress(self,input_path):
        file_name,file_extension=os.path.splitext(input_path)
        output_path=file_name+"Decompressed"+".txt"
        with open(input_path,"rb") as file,open(output_path,"w")as output:
            bit_string=""
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bit=bin(byte)[2:].rjust(8,"0")
                bit_string+=bit
                byte=file.read(1)
            actual_text=self.__remove_padding(bit_string)

            decoded_text=self.__decoding_text(actual_text)
            output.write(decoded_text)

            print("Decompressed Successfully")



kamal=HuffmanCoding(r'C:\Users\kamal\Documents\Hell.txt')
result=kamal.compress()
print(result)
kamal.decompress(result)

