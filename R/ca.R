#######################################
# MICS-3 Computational Statistics
# Correspondance Analysis of two-way contingency tables
# R.B. Nay 2018
# https://en.wikipedia.org/wiki/Correspondence_analysis
#######################################
ca = function(C,axis1=1,axis2=2,axis3=3,hlabels=0.75) {
# C is a contingency table as m x n matrix with given row and col names.
# computing the eigen decomposition on the samllest of the dimensions
if (dim(C)[1] < dim(C)[2]) {C = t(C) } 
m = length(rownames(C))
n = length(colnames(C))
nc = sum(C)
S = 1/nc*C
none = as.matrix(rep(1,n))
rowsum = S %*% none
mone = as.matrix(rep(1,m))
colsum = t(mone) %*% S
M = (S - rowsum %*% colsum)/sqrt(rowsum %*% colsum)
svdM = svd(M)
# scaling and rotating the row vectors of M
Wm = diag(as.vector(1/sqrt(rowsum)))
Fm = Wm %*% svdM$u %*% diag(svdM$d)
rownames(Fm) = rownames(C)
colnames(Fm) = colnames(C)
# scaling and rotating the column vectors of M
Wn = diag(as.vector(1/sqrt(colsum)))
Fn = Wn %*% svdM$v %*% diag(svdM$d)
rownames(Fn) = colnames(C)
colnames(Fn) = colnames(C)
# computing the eigenvalues of t(C) %*% C
val = svdM$d[1:n]^2/sum(svdM$d[1:n]^2)
nval = length(val)
# starting the graphic output 
par(mfrow=c(2,2))
# axes 1 and 2
a1 = axis1
a2 = axis2
minx1= min(c(Fn[,a1],Fm[,a1]))
maxx1= max(c(Fn[,a1],Fm[,a1]))
miny2= min(c(Fn[,a2],Fm[,a2]))
maxy2= max(c(Fn[,a2],Fm[,a2]))
plot(Fn[,a1],Fn[,a2],"n",xlab=paste("axis ",a1,":",val[a1]*100,"%"),
      ylab=paste("axis ",a2,":",val[a2]*100,"%"), ylim= c(miny2,maxy2), xlim=c(minx1,maxx1))
text(Fn[,a1],Fn[,a2],rownames(Fn),cex=hlabels)
text(Fm[,a1],Fm[,a2],rownames(Fm),col='red',cex=hlabels)
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
# axes 2 and 3
a1 = axis2
a2 = axis3
minx2= min(c(Fn[,a1],Fm[,a1]))
maxx2= max(c(Fn[,a1],Fm[,a1]))
miny3= min(c(Fn[,a2],Fm[,a2]))
maxy3= max(c(Fn[,a2],Fm[,a2]))
plot(Fn[,a1],Fn[,a2],"n",xlab=paste("axis ",a1,":",val[a1]*100,"%"),
      ylab=paste("axis ",a2,":",val[a2]*100,"%"), ylim= c(miny3,maxy3), xlim=c(minx2,maxx2))
text(Fn[,a1],Fn[,a2],rownames(Fn),cex=hlabels)
text(Fm[,a1],Fm[,a2],rownames(Fm),col='red',cex=hlabels)
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
# axes 1 and 3
a1 = axis1
a2 = axis3
minx1= min(c(Fn[,a1],Fm[,a1]))
maxx1= max(c(Fn[,a1],Fm[,a1]))
miny3= min(c(Fn[,a2],Fm[,a2]))
maxy3= max(c(Fn[,a2],Fm[,a2]))
plot(Fn[,a1],Fn[,a2],"n",xlab=paste("axis ",a1,":",val[a1]*100,"%"),
      ylab=paste("axis ",a2,":",val[a2]*100,"%"), ylim= c(miny3,maxy3), xlim=c(minx1,maxx1))
text(Fn[,a1],Fn[,a2],rownames(Fn),cex=hlabels)
text(Fm[,a1],Fm[,a2],rownames(Fm),col='red',cex=hlabels)
abline(h=0,lty=2,col="gray")
abline(v=0,lty=2,col="gray")
# barplot of the eigenvalues
barplot(val[1:nval]*100,names.arg=1:nval,main="Axis inertia (in %)",col="orangered")
}
