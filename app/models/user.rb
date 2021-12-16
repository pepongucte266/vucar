class User < ApplicationRecord
  ATTR_CHANGE = %i(name email password password_confirmation).freeze
  before_save :downcase_email
  validates :name, presence: true, length: {maximum: Settings.max_name}
  validates :email, presence: true, length: {maximum: Settings.max_email},
    format: {with: Settings.email_regex},
    uniqueness: true
  validates :password, presence: true, length: {minimum: Settings.min_password}
  has_secure_password

  private
  def downcase_email
    email.downcase!
  end
end
