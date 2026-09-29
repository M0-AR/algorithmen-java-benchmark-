import java.util.*;
import java.nio.file.*;
public class BenchAll {
  static long cmp=0;
  static void qs(int[] a,int lo,int hi){int i=lo,j=hi,x=a[(lo+hi)/2];
    while(i<=j){while(a[i]<x){cmp++;i++;}cmp++;while(a[j]>x){cmp++;j--;}cmp++;
      if(i<=j){int t=a[i];a[i]=a[j];a[j]=t;i++;j--;}}}
    if(lo<j)qs(a,lo,j); if(i<hi)qs(a,i,hi);}
  public static void main(String[] s) throws Exception {
    int[] a={5,7,0,3,4,2,6,1};
    qs(a,0,a.length-1);
    System.out.println("java quicksort ok: "+Arrays.toString(a)+" cmp="+cmp);
  }
}
