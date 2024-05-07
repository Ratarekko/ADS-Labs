#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node* next;
} Node;

Node* createNode(int data) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->data = data;
    newNode->next = NULL;
    return newNode;
}

Node* insertNode(Node* head, int data) {
    if (head == NULL)
        return createNode(data);
    Node* temp = head;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = createNode(data);
    return head;
}

void printList(Node* head) {
    Node* temp = head;
    printf("\nResult: ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next;
    }
    printf("\n");
}

Node* rotate(Node* head, int k) {
    if (k == 0)
        return head;
    Node* current = head;
    int count = 1;
    while (count < k && current != NULL) {
        current = current->next;
        count++;
    }
    if (current == NULL)
        return head;
    Node* kthNode = current;
    while (current->next != NULL)
        current = current->next;
    current->next = head;
    head = kthNode->next;
    kthNode->next = NULL;
    return head;
}

void freeList(Node** head) {
    Node* current = *head;
    Node* next;
    while (current != NULL) {
        next = current->next;
        free(current);
        current = next;
    }
    *head = NULL;
}

int main() {
    Node* head = NULL;
    int n, k, data;
    printf("Enter the number of nodes:");
    scanf("%d", &n);
    printf("Enter the node values:");
    for (int i = 0; i < n; i++) {
        scanf("%d", &data);
        head = insertNode(head, data);
    }
    printf("Enter the number of positions to rotate:");
    scanf("%d", &k);
    head = rotate(head, k);
    printList(head);
    freeList(&head);
    return 0;
}
