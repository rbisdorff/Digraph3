# pca do it yourself
# RB November 2011
# compstat MICS 3
# linear algebra lesson
#########################3
centerReduce = function(x) {
  
  (x-colMeans(x))/(sapply(x,sd)*sqrt(length(t(x))))
}
center = function(x) {
  
  (x-colMeans(x))
}
####
pcacov = function(Xin) {
X = as.matrix(x)
# cov is working on the columns of t(X)
A = cov(t(X))
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=X,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pcac = function(Xin) {
# center and reduce 
X = as.matrix(center(Xin))
# covariance of the lines of X
A = X %*% t(X)
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=X,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pcacr = function(Xin) {
# center and reduce 
X = as.matrix(centerReduce(Xin))
# covariance of the lines
A = X %*% t(X)
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=X,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pca = function(Xin) {
# center and reduce 
X = as.matrix(Xin)
# covariance on the lines
A = X %*% t(X)
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=X,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pcaPlot = function(pcaRes) {
val = pcaRes$val
nval = length(val)
par(mfrow=c(2,2))
if (pcaRes$cr == 0){ 
a1 = 1
a2 = 2
a3 = 3}
else {
a1 = 2
a2 = 3
a3 = 4
}
plot(pcaRes$P[a1,],pcaRes$P[a2,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 2:",val[a2]*100,"%"),asp=1)
text(pcaRes$P[a1,],pcaRes$P[a2,],rownames(pcaRes$x))
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
plot(pcaRes$P[a2,],pcaRes$P[a3,],"n",xlab=paste("axis 2:",val[a2]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)
text(pcaRes$P[a2,],pcaRes$P[a3,],rownames(pcaRes$x))
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
plot(pcaRes$P[a1,],pcaRes$P[a3,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)
text(pcaRes$P[a1,],pcaRes$P[a3,],rownames(pcaRes$x))
abline(h=0,v=0,lty=2,col="gray")
barplot(val[a1:nval]*100,names.arg=a1:nval,main="Axis inertia (in %)",col="orangered")
}

