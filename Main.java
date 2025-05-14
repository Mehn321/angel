import javax.swing.JOptionPane;

public class Main {
    public static void main(String[] args) {

        String stringnum1 = JOptionPane.showInputDialog("enter the first number");
        String stringnum2 = JOptionPane.showInputDialog("enter the second number");
        int num1=Integer.parseInt(stringnum1);
        int num2=Integer.parseInt(stringnum2);
        

        JOptionPane.showMessageDialog(null,num1+"+"+num2+"= "+(num1+num2));
    }
}









































        // String name= JOptionPane.showInputDialog("enter your name: ");
        // JOptionPane.showMessageDialog(null, "your name is "+name);