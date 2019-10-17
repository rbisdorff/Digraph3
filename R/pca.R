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
pcacov = function(Min,linewise=FALSE) {
M = as.matrix(Min)
# cov is by default working on the columns of M
if (linewise)
    { A = cov(t(M)) }
else
    { A = cov(M) } 
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=M,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pcac = function(Min,linewise=TRUE) {
# center
M = as.matrix(center(Min))
# covariance of the columns
if (linewise)
    { A = M %*% t(M) }
else
    { A = t(M) %*% M }
# eigen vectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=M,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pcacr = function(Min,linewise=TRUE) {
# center and reduce 
M = as.matrix(centerReduce(Min))
# covariance
if (linewise)
   {A = M %*% t(M) }
else
   {A = t(M) %*% M}
# eigenvectors and values
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=M,eig=E,a=A,P=P,val=valprop,cr=0)
pcaRes
}
####
pca = function(Min,linewise=TRUE,covariance=TRUE) {
# no transformation
M = as.matrix(Min)
# covariance on the columns
if (linewise)
  {if (covariance)
    {A = M %*% t(M)}
   else 
    {A = M} }
else
  {if (covariance)
    { A = t(M) %*% M }
   else 
    {A = t(M)} }
# eigen vectors X and eigenvalues 
E = eigen(A, symmetric=TRUE)
P = E$values * t(E$vectors)
valprop = E$values/sum(E$values)
pcaRes = list(x=M,eig=E,a=A,P=P,val=valprop)
pcaRes
}
####
pcaPlot = function(pcaRes,a1=1,a2=2,a3=3) {
val = pcaRes$val
nval = length(val)
par(mfrow=c(2,2))
plot(pcaRes$P[a1,],pcaRes$P[a2,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 2:",val[a2]*100,"%"),asp=1)
text(pcaRes$P[a1,],pcaRes$P[a2,],rownames(pcaRes$a))
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
plot(pcaRes$P[a2,],pcaRes$P[a3,],"n",xlab=paste("axis 2:",val[a2]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)
text(pcaRes$P[a2,],pcaRes$P[a3,],rownames(pcaRes$a))
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
plot(pcaRes$P[a1,],pcaRes$P[a3,],"n",xlab=paste("axis 1:",val[a1]*100,"%"),ylab=paste("axis 3:",val[a3]*100,"%"),asp=1)
text(pcaRes$P[a1,],pcaRes$P[a3,],rownames(pcaRes$a))
abline(h=0,v=0,lty=2,col="gray")
barplot(val[a1:nval]*100,names.arg=a1:nval,main="Axis inertia (in %)",col="orangered")
}

