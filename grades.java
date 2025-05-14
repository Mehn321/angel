// import javax.swing.*;

// class Grades{
// 	public static void main(String[] args) {
// 		double PrelimGrade =74.9;
// 		double MidtermGrade =82.0;
// 		double SemiFinalGrade =71.0;
// 		double FinalGrade =81.0;
// 		double average=0;
		
// 		//solve for the average
// 		average=(PrelimGrade+MidtermGrade+SemiFinalGrade+FinalGrade)/4;
		
// 		if (average>=75){
// 			JOptionPane.showMessageDialog(null, "Average" + average+" \n You Passed");
// 		}
// 			else{
// 				JOptionPane.showMessageDialog(null, "Average" + average+" You Failed");
				
				
// 			}
// 		}
// 	}


// import javax.swing.*;
// import java.util.Scanner;

// class Grades {
//     public static void main(String[] args) {
//         Scanner input = new Scanner(System.in);
//         double PrelimGrade, MidtermGrade, SemiFinalGrade, FinalGrade, average;

//         System.out.print("Enter Prelim Grade: ");
//         PrelimGrade = input.nextDouble();
//         System.out.print("Enter Midterm Grade: ");
//         MidtermGrade = input.nextDouble();
//         System.out.print("Enter Semifinal Grade: ");
//         SemiFinalGrade = input.nextDouble();
//         System.out.print("Enter Final Grade: ");
//         FinalGrade = input.nextDouble();

//         average = (PrelimGrade + MidtermGrade + SemiFinalGrade + FinalGrade) / 4;

//         String message = "";
//         if (average >= 97) message = "1.00";
//         else if (average >= 94) message = "1.25";
//         else if (average >= 91) message = "1.50";
//         else if (average >= 88) message = "1.75";
//         else if (average >= 85) message = "2.00";
//         else if (average >= 82) message = "2.25";
//         else if (average >= 79) message = "2.50";
//         else if (average >= 76) message = "2.75";
//         else if (average >= 75) message = "3.00";
//         else message = "5.00";

//         JOptionPane.showMessageDialog(null, "Average: " + average + ", Output: " + message);
//         input.close();
//     }
// }





// import java.util.Scanner;

// class CartesianCoordinates {
//     public static void main(String[] args) {
//         Scanner input = new Scanner(System.in);
//         int x, y;

//         System.out.print("Enter the x-coordinate: ");
//         x = input.nextInt();
//         System.out.print("Enter the y-coordinate: ");
//         y = input.nextInt();

//         String quadrant;
//         if (x > 0 && y > 0) {
//             quadrant = "Quadrant I";
//         } else if (x < 0 && y > 0) {
//             quadrant = "Quadrant II";
//         } else if (x < 0 && y < 0) {
//             quadrant = "Quadrant III";
//         } else if (x > 0 && y < 0) {
//             quadrant = "Quadrant IV";
//         } else if (x == 0 && y == 0) {
//             quadrant = "Origin";
//         } else if (x == 0) {
//             quadrant = "y-axis";
//         } else {
//             quadrant = "x-axis";
//         }

//         System.out.println("The point (" + x + ", " + y + ") is in " + quadrant);
//         input.close();
//     }
// }







import java.util.Scanner;

class ArithmeticSwitch {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        int choice, num1, num2;
        double result = 0;

        System.out.println("Select an operation:");
        System.out.println("1. Add");
        System.out.println("2. Subtract");
        System.out.println("3. Multiply");
        System.out.println("4. Divide");
        System.out.println("5. Exit");
        System.out.print("Enter your choice: ");
        choice = input.nextInt();

        switch (choice) {
            case 1:
                System.out.print("Enter two numbers: ");
                num1 = input.nextInt();
                num2 = input.nextInt();
                result = num1 + num2;
                System.out.println("Result: " + result);
                break;
            case 2:
                System.out.print("Enter two numbers: ");
                num1 = input.nextInt();
                num2 = input.nextInt();
                result = num1 - num2;
                System.out.println("Result: " + result);
                break;
            case 3:
                System.out.print("Enter two numbers: ");
                num1 = input.nextInt();
                num2 = input.nextInt();
                result = num1 * num2;
                System.out.println("Result: " + result);
                break;
            case 4:
                System.out.print("Enter two numbers: ");
                num1 = input.nextInt();
                num2 = input.nextInt();
                if (num2 == 0) {
                    System.out.println("Result:" + result);
                } else {
                    result = (double) num1 / num2;
                    System.out.println("Result: " + result);
                }
                break;
            case 5:
                System.out.println("Exiting program.");
                break;
            default:
                System.out.println("Operation");
        }
        input.close();
    }
}