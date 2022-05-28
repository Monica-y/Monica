#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

// Definition for singly-linked list.
struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};
class Solution {
public:
    ListNode* mergeSort(ListNode* A,ListNode*B){
        ListNode*res = new ListNode();
        ListNode*now = new ListNode();
        now = res;
        int elem_a,elem_b;
        while(A!=nullptr||B!=nullptr){
            if(A!=nullptr){
                elem_a = A->val;
            }else{
                elem_a = 2e4;
            }
            if(B!=nullptr){
                elem_b = B->val;
            }else{
                elem_b = 2e4;
            }
            if(elem_a<elem_b){
                now->next = A;
                now = A;
                A = A->next;
            }else{
                now->next = B;
                now = B;
                B = B->next;
            }
        }
        return res->next;
    }
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        int len = lists.size();
        if(len<2){
            return lists[0];
        }
        auto res = mergeSort(lists[0],lists[1]);
        for(int i = 2;i<len;i++){
            res = mergeSort(res,lists[i]);
        }
        return res;
    }
};
ListNode* create_list(vector<int>data){
    ListNode* A = new ListNode();
    ListNode* now = A;
    for(int i = 0;i<data.size();i++){
        ListNode* insert = new ListNode();
        now->next = insert;
        insert->val = data[i];
        now = insert;
    }
    now->next = nullptr;
    return A->next;
}
int main(){
    Solution* so = new Solution();
    vector<int>list1 = {1,4,5};
    vector<int>list2 = {1,3,4};
    vector<int>list3 = {2,6};
    vector<ListNode*> values;
    values.push_back(create_list(list1));
    values.push_back(create_list(list2));
    values.push_back(create_list(list3));
    so->mergeKLists(values);
    return 0;
}
