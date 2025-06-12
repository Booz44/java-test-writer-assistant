package com.example.calculator;

import java.util.List;
import java.util.ArrayList;

/**
 * Simple calculator class for demonstration purposes.
 * Provides basic arithmetic operations and some utility methods.
 */
public class Calculator {
    
    private List<Double> history;
    private boolean debugMode;
    
    public Calculator() {
        this.history = new ArrayList<>();
        this.debugMode = false;
    }
    
    /**
     * Adds two numbers and returns the result.
     */
    public double add(double a, double b) {
        double result = a + b;
        history.add(result);
        if (debugMode) {
            System.out.println("Addition: " + a + " + " + b + " = " + result);
        }
        return result;
    }
    
    /**
     * Subtracts the second number from the first.
     */
    public double subtract(double a, double b) {
        double result = a - b;
        history.add(result);
        if (debugMode) {
            System.out.println("Subtraction: " + a + " - " + b + " = " + result);
        }
        return result;
    }
    
    /**
     * Multiplies two numbers.
     */
    public double multiply(double a, double b) {
        double result = a * b;
        history.add(result);
        if (debugMode) {
            System.out.println("Multiplication: " + a + " * " + b + " = " + result);
        }
        return result;
    }
    
    /**
     * Divides the first number by the second.
     * Throws IllegalArgumentException if divisor is zero.
     */
    public double divide(double a, double b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        double result = a / b;
        history.add(result);
        if (debugMode) {
            System.out.println("Division: " + a + " / " + b + " = " + result);
        }
        return result;
    }
    
    /**
     * Returns the square root of a number.
     * Throws IllegalArgumentException for negative numbers.
     */
    public double sqrt(double number) {
        if (number < 0) {
            throw new IllegalArgumentException("Cannot calculate square root of negative number");
        }
        double result = Math.sqrt(number);
        history.add(result);
        return result;
    }
    
    /**
     * Returns the calculation history.
     */
    public List<Double> getHistory() {
        return new ArrayList<>(history);
    }
    
    /**
     * Clears the calculation history.
     */
    public void clearHistory() {
        history.clear();
    }
    
    /**
     * Validates if a number is within acceptable range.
     */
    public boolean validateNumber(double number) {
        return !Double.isNaN(number) && !Double.isInfinite(number);
    }
    
    /**
     * Sets debug mode on or off.
     */
    public void setDebugMode(boolean enabled) {
        this.debugMode = enabled;
    }
    
    /**
     * Gets the current debug mode setting.
     */
    public boolean isDebugMode() {
        return debugMode;
    }
}