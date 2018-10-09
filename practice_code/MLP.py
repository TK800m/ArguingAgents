import numpy as np
import tensorflow as tf

class Network:
    def __init__(self, n_features, architecture, n_outputs, learning_rate):
        tf.reset_default_graph()
        # inputs
        self.x = tf.placeholder(tf.float32, (None, n_features))
        # ground truth labels
        self.labels = tf.placeholder(tf.float32, (None, n_outputs))
        
        # construct the hidden layers specified in the layers parameter
        layers = []
        # store the previous outputs to be used as inputs for the next layers
        layers.append(self.x)
        
        for i in range(len(architecture) - 1):
            weights = tf.get_variable(name = "weights_" + str(i), shape = [architecture[i], architecture[i + 1]], initializer=tf.random_normal_initializer)
            bias = tf.get_variable(name = "bias_" + str(i), shape = [1, architecture[i + 1]], initializer=tf.random_normal_initializer)
            output = tf.nn.sigmoid(tf.add(tf.matmul(layers[i], weights), bias))
            layers.append(output)
            
        
        
        
        # hidden weights
        #self.hidden_w = tf.get_variable(name = "hidden_weights", shape = [n_features, n_hidden], initializer=tf.random_normal_initializer)
        # output weights
        self.output_w = tf.get_variable(name = "output_weights", shape = [architecture[-1], n_outputs], initializer=tf.random_normal_initializer)
        # hidden bias
        #self.hidden_bias = tf.get_variable(name = "hidden_bias", shape = [1, n_hidden], initializer=tf.random_normal_initializer)
        # output bias
        self.output_bias = tf.get_variable(name = "output_bias", shape = [1, n_outputs], initializer = tf.random_normal_initializer)
        # hidden activation
        #h = tf.nn.sigmoid(tf.add(tf.matmul(self.x, self.hidden_w), self.hidden_bias))
        # network output
        self.y = tf.nn.sigmoid(tf.add(tf.matmul(layers[-1], self.output_w), self.output_bias))
        #loss   
        self.loss = tf.reduce_mean(tf.squared_difference(self.labels,
    self.y))
        # optimization procedure
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
        self.train_op = optimizer.minimize(self.loss)
        # Initializing the variables
        init = tf.global_variables_initializer()
      
        self.session = tf.Session()
        self.session.run(init)
        
    def accuracy(self, x, y):
        predictions = self.test(x)
        predictions[predictions >= 0.5] = 1.0
        predictions[predictions < 0.5] = 0.0
        errors = np.count_nonzero(predictions - y)
        correct = len(y) - errors
        accuracy = correct / len(y)
        
        return accuracy
        
    def train(self, x, labels, epochs, batch_size):
        n_batches = int(len(x) / batch_size)
        print(len(x))
        for j in range(epochs):
            avg_cost = 0
            avg_acc = 0
            for i in range(n_batches):
                batchX = x[i * batch_size:(i + 1) * batch_size]
                batchY = labels[i * batch_size:(i + 1) * batch_size]
                cost, _ = self.session.run([self.loss, self.train_op], feed_dict = {self.x: batchX, self.labels: batchY})
                avg_cost += cost
                avg_acc += self.accuracy(batchX, batchY)
            # if there is still data left, feed it as the final mini batch    
            if((i + 1) * batch_size != len(x)):
                batchX = x[(i + 1) * batch_size:]
                batchY = labels[(i + 1) * batch_size:]
                cost, _ = self.session.run([self.loss, self.train_op], feed_dict = {self.x: batchX, self.labels: batchY})    
                avg_cost += cost
                avg_acc += self.accuracy(batchX, batchY)
                avg_cost = avg_cost / (n_batches + 1)
                avg_acc = avg_acc / (n_batches + 1)
            else:
                avg_cost = avg_cost / n_batches
                avg_acc = avg_acc / n_batches
                    
            if(j % 10 == 0):   
                print("Iteration: {0}, average cost: {1}, average accuracy: {2}".format(j, avg_cost, avg_acc))
        
    def train_val(self, x, labels, val, val_labels, epochs, batch_size):
        train_costs = []
        val_costs = []
        n_batches = int(len(x) / batch_size)
        for j in range(epochs):
            avg_cost = 0
            for i in range(n_batches):
                batchX = x[i * batch_size:(i + 1) * batch_size]
                batchY = labels[i * batch_size:(i + 1) * batch_size]
                cost, _ = self.session.run([self.loss, self.train_op], feed_dict = {self.x: batchX, self.labels: batchY})  
                avg_cost += cost
                
            # if there is still data left, feed it as the final mini batch    
            if((i + 1) * batch_size != len(x)):
                batchX = x[(i + 1) * batch_size:]
                batchY = labels[(i + 1) * batch_size:]
                cost, _ = self.session.run([self.loss, self.train_op], feed_dict = {self.x: batchX, self.labels: batchY})    
                avg_cost += cost
                avg_cost = avg_cost / (n_batches + 1)
            else:
                avg_cost = avg_cost / n_batches
           
            
            if(j % 1000 == 0): 
                print("Train cost:", avg_cost )
                train_acc = self.accuracy(x, labels)
                train_costs.append(train_acc)                                 
                val_acc = self.accuracy(val, val_labels)
                val_costs.append(val_acc)
                print("-----------------------------------------------------")
                print("Iteration: {0}, train accuracy: {1}, val accuracy: {2}".format(j, train_acc, val_acc))
        return train_costs, val_costs
    
    def get_weights(self):
        return self.w, self.b
    
    def test(self, x):
        return self.y.eval(feed_dict = {self.x: x}, session = self.session)