use maindb;

create table users(
    role varchar(20),
    class varchar(100),
    chat_id varchar(100) primary key,
    job varchar(30)
);

create table parentsQuestions(
    chat_id varchar(100),
    question varchar(200),
    FOREIGN KEY (chat_id) REFERENCES users(chat_id)
);

create table parentsQuestionsQueue(
    chat_id varchar(100),
    question varchar(200),
    FOREIGN KEY (chat_id) REFERENCES users(chat_id)
);

create table QA(
    chat_id varchar(100),
    answer varchar(200),
    question varchar(200),
	keywords varchar(200),
	FOREIGN KEY (chat_id) REFERENCES users(chat_id)
);
