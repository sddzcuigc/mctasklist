import sys
import json
import os
import base64
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QLabel, QMessageBox, QFileDialog, QProgressBar, QHBoxLayout, QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

# 史蒂夫图片的 base64 编码数据
steve_base64 = '''/9j/4AAQSkZJRgABAQEAAAAAAAD/4QAuRXhpZgAATU0AKgAAAAgAAkAAAAMAAAABAAsAAEABAAEAAAABAAAAAAAAAAD/2wBDAAoHBwkHBgoJCAkLCwoMDxkQDw4ODx4WFxIZJCAmJSMgIyIoLTkwKCo2KyIjMkQyNjs9QEBAJjBGS0U+Sjk/QD3/2wBDAQsLCw8NDx0QEB09KSMpPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT3/wAARCAHRAV4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD2WiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooqvd6haWERkvLqC3QfxSyBR+tAFiiuP1L4n+HbDKpcyXbjjbboSP++jgfka5bUvjLcvuXTNMjjHQPO5c/98jH8zUOcV1LVOT6HrNVL7VbHTE3315Bbrj/AJaSBf514NqXj3xFqeRNqUsaH+CD92B+XP55rn5JHlcvIzO7HJZjkmodZdEaKi+rPcNR+Knh6xysEk1447Qx8fm2P0zXK6l8Y76XK6bp8MA6bpmMh/IYA/WvN6KzdSTNFSijV1nxLqfiCTfqVwJcHgCNVx+Qr0T4eeLltba30nUGVIsAQSngKT/CfqTwff8ALyat2H/j3j/3R/Ks+dxaZTgnGx9E0V594G8Z+Z5elapJ84G2CZj970U+/oe/Tr19BrrhNSV0ckouLswoooqyQooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooqK5kaK1lkXG5ELDPsKAJeahuby3sojLdTxQxjq0jhQPxNeFal8SfEeobl+2i2jb+G3UJj/gX3v1rmrm6uLyUy3U8s0h6tI5Yn8TWLqrobKi+rPddS+JXhzTtwF4bpx/DboX/8e+7+tcrqXxmc7l0vTFX0e4fP/jo/xry6is3VkaKlFbnTaj8Q/Eeo5Dai0EZ/htwI8fiPm/WudmmluZDJPI8sjclnYsT+JqOiocm9zRRS2CiiikMKKKKACiiigBa2oP8AUR/7o/lWJW5b820f+6KmY0SdMEda9M8EeM/typpmpyf6SPlilY/6z2P+179/r18ypQShDKSGByCOMUQm4PQU4KasfQ1FcX4J8YjVY00/UHAvVGEc/wDLUD/2Yfr1rtK7oyUldHFKLi7MKKKKokKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAqC+/wCPC4/65N/Kp6hu1aSzmRRlmjYAevFAI+YKKSiuE7haKSigYtFOjiklO2NGdvRRmr8OgahNjFuUHq5C4/rScktxqLeyM6iugh8JSnBnuVX1CDd/OtGHwxYRYLiSU/7bY/lUuokaKjJnHVYhsLu5x5NvKwP8QXj867iGwtbbHk28SEdwoz+dWKh1eyLVDuzjofC9/Jgv5cQ/2mz/ACqlqNkdOvGty+8qASwGOozXfVxvicAawSP4o1J/z+FOE23ZiqU1FXRk1tW3/HtF/uisStq2/wCPaP8A3RVTMUS0UUVBQ6ORopFkjZldTuVgcEGvV/Bni9NahWzvGC38Y65wJQO49/Ufj7DyanwzS20yTQO0ciHcrKcEGtKc3BmdSCmj6EorI8LapLrHh61vLgASuCG29CQxGfxxmteu9O6ucTVnYKKKKYgooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKD0P0ooPQ/SgD5ZrR0zR5dV8wpIiLGQG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'''

class TaskWidget(QWidget):
    def __init__(self, task_index, task_description, task_experience, task_reward, task_difficulty, parent=None):
        super().__init__(parent)
        self.task_index = task_index
        self.parent_app = parent
        
        layout = QHBoxLayout()
        
        self.task_label = QLabel(f"{task_index + 1}. {task_description} - 难度: {task_difficulty} - {task_experience} 经验值 - {task_reward}", self)
        layout.addWidget(self.task_label)
        
        self.reset_button = QPushButton('重置', self)
        self.reset_button.clicked.connect(self.resetTask)
        layout.addWidget(self.reset_button)
        
        self.delete_button = QPushButton('删除', self)
        self.delete_button.clicked.connect(self.deleteTask)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
    
    def resetTask(self):
        if self.parent_app:
            self.parent_app.resetTask(self.task_index)
    
    def deleteTask(self):
        if self.parent_app:
            self.parent_app.deleteTask(self.task_index)

class TodoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.level = 1
        self.experience = 0
        self.rewards = {}
        self.initUI()
        self.loadTasks()
    
    def initUI(self):
        self.setWindowTitle('MC挑战清单by崔护')
        
        layout = QVBoxLayout()
        
        # 史蒂夫图片
        self.steve_label = QLabel(self)
        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(steve_base64))
        self.steve_label.setPixmap(pixmap.scaled(400, 100, Qt.KeepAspectRatio))
        self.steve_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.steve_label)
        
        # 任务输入
        self.taskInput = QLineEdit(self)
        self.taskInput.setPlaceholderText('输入任务描述（如：完成一次电脑知识学习挑战（奖励：20 经验值，1.5 铁块方块））')
        layout.addWidget(self.taskInput)
        
        # 任务经验输入
        self.expInput = QLineEdit(self)
        self.expInput.setPlaceholderText('输入经验值（如：15）')
        layout.addWidget(self.expInput)
        
        # 任务奖励输入
        self.rewardInput = QLineEdit(self)
        self.rewardInput.setPlaceholderText('输入奖励（如：1.5 个铁方块）')
        layout.addWidget(self.rewardInput)
        
        # 任务难度输入
        self.difficultyInput = QLineEdit(self)
        self.difficultyInput.setPlaceholderText('输入任务难度（如：1-5）')
        layout.addWidget(self.difficultyInput)
        
        # 添加任务按钮
        addButton = QPushButton('添加任务', self)
        addButton.clicked.connect(self.addTask)
        layout.addWidget(addButton)
        
        # 导入任务按钮
        importButton = QPushButton('导入任务', self)
        importButton.clicked.connect(self.importTasks)
        layout.addWidget(importButton)
        
        # 导出配置文件按钮
        exportButton = QPushButton('导出配置文件', self)
        exportButton.clicked.connect(self.exportTasks)
        layout.addWidget(exportButton)
        
        # 任务列表
        self.taskList = QListWidget(self)
        layout.addWidget(self.taskList)
        
        # 排序任务按钮
        sortButton = QPushButton('按难度排序', self)
        sortButton.clicked.connect(self.sortTasksByDifficulty)
        layout.addWidget(sortButton)
        
        # 完成任务按钮
        completeButton = QPushButton('完成任务', self)
        completeButton.clicked.connect(self.completeTask)
        layout.addWidget(completeButton)
        
        # 状态显示
        self.statusLabel = QLabel(self)
        layout.addWidget(self.statusLabel)
        
        # 经验值进度条
        self.expProgressBar = QProgressBar(self)
        layout.addWidget(self.expProgressBar)
        
        # 离下一等级需求经验标签
        self.nextLevelExpLabel = QLabel(self)
        layout.addWidget(self.nextLevelExpLabel)
        
        self.setLayout(layout)
        self.updateStatus()
    
    def addTask(self):
        description = self.taskInput.text()
        experience = self.expInput.text()
        reward = self.rewardInput.text()
        difficulty = self.difficultyInput.text()
        
        if not description or not experience.isdigit() or not reward or not difficulty.isdigit():
            QMessageBox.warning(self, '输入错误', '请输入有效的任务详情')
            return
        
        task = {
            "description": description,
            "experience": int(experience),
            "reward": reward,
            "difficulty": int(difficulty),
            "completed": False
        }
        self.tasks.append(task)
        self.updateTaskList()
        
        self.taskInput.clear()
        self.expInput.clear()
        self.rewardInput.clear()
        self.difficultyInput.clear()
        self.saveTasks()
    
    def importTasks(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "打开任务文件", "", "JSON 文件 (*.json);;所有文件 (*)", options=options)
        if fileName:
            with open(fileName, 'r', encoding='utf-8') as file:
                tasks = json.load(file)
                for task in tasks:
                    description, experience, reward, difficulty = task['description'], task['experience'], task['reward'], task['difficulty']
                    task = {
                        "description": description,
                        "experience": int(experience),
                        "reward": reward,
                        "difficulty": int(difficulty),
                        "completed": False
                    }
                    self.tasks.append(task)
                self.updateTaskList()
                self.saveTasks()
    
    def exportTasks(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "导出配置文件", "", "JSON 文件 (*.json);;所有文件 (*)", options=options)
        if fileName:
            tasks_data = {
                'tasks': self.tasks,
                'level': self.level,
                'experience': self.experience,
                'rewards': self.rewards
            }
            with open(fileName, 'w', encoding='utf-8') as file:
                json.dump(tasks_data, file, ensure_ascii=False, indent=4)
            QMessageBox.information(self, '导出成功', f'配置文件已成功导出到 {fileName}')
    
    def completeTask(self):
        selectedTaskIndex = self.taskList.currentRow()
        
        if selectedTaskIndex == -1 or self.tasks[selectedTaskIndex]['completed']:
            QMessageBox.warning(self, '选择错误', '请选择一个有效的任务完成')
            return
        
        self.tasks[selectedTaskIndex]['completed'] = True
        self.gainExperience(self.tasks[selectedTaskIndex]['experience'])
        self.addReward(self.tasks[selectedTaskIndex]['reward'])
        
        self.updateStatus()
        self.updateTaskList()
        self.saveTasks()
    
    def resetTask(self, index):
        self.tasks[index]['completed'] = False
        self.updateTaskList()
        self.saveTasks()
    
    def deleteTask(self, index):
        del self.tasks[index]
        self.updateTaskList()
        self.saveTasks()
    
    def gainExperience(self, exp):
        self.experience += exp
        self.checkLevelUp()
    
    def addReward(self, reward):
        try:
            parts = reward.split()
            reward_value = float(parts[0])
            reward_name = ' '.join(parts[1:])
        except (IndexError, ValueError):
            return
        
        reward_name = reward_name.lower()
        if reward_name in self.rewards:
            self.rewards[reward_name] += reward_value
        else:
            self.rewards[reward_name] = reward_value
    
    def checkLevelUp(self):
        requiredExp = self.level ** 2 + self.level * 5
        while self.experience >= requiredExp:
            self.experience -= requiredExp
            self.level += 1
            QMessageBox.information(self, '升级', f'恭喜！你已达到等级 {self.level}')
            requiredExp = self.level ** 2 + self.level * 5
    
    def updateTaskList(self):
        self.taskList.clear()
        for index, task in enumerate(self.tasks):
            task_widget = TaskWidget(index, task['description'], task['experience'], task['reward'], task['difficulty'], self)
            list_item = QListWidgetItem()
            list_item.setSizeHint(task_widget.sizeHint())
            self.taskList.addItem(list_item)
            self.taskList.setItemWidget(list_item, task_widget)
    
    def sortTasksByDifficulty(self):
        self.tasks.sort(key=lambda t: t['difficulty'])
        self.updateTaskList()
    
    def updateStatus(self):
        reward_summary = ', '.join([f"{item.upper()} x{round(count, 2)}" for item, count in sorted(self.rewards.items())])
        
        self.statusLabel.setText(f"等级: {self.level}, 经验值: {self.experience}, 奖励: {reward_summary}")
        
        required_exp = self.level ** 2 + self.level * 5
        self.expProgressBar.setMaximum(required_exp)
        self.expProgressBar.setValue(self.experience)
        
        remaining_exp = required_exp - self.experience
        self.nextLevelExpLabel.setText(f"离下一等级还需经验: {remaining_exp}")

    def saveTasks(self):
        tasks_data = {
            'tasks': self.tasks,
            'level': self.level,
            'experience': self.experience,
            'rewards': self.rewards
        }
        with open('tasks_data.json', 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=4)

    def loadTasks(self):
        if os.path.exists('tasks_data.json'):
            with open('tasks_data.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.tasks = data.get('tasks', [])
                self.level = data.get('level', 1)
                self.experience = data.get('experience', 0)
                self.rewards = data.get('rewards', {})
                self.updateTaskList()
                self.updateStatus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoListApp()
    ex.show()
    sys.exit(app.exec_())
